import fetch from "node-fetch";
import * as fs from "fs";

type SpiderCommand = {
	url : string,
	recursive : boolean,
	level : number,
	path : string
}

function getSpiderCommand() : SpiderCommand | undefined
{
	let command : SpiderCommand = {
		url : "",
		recursive : false,
		level : 5,
		path : "./data/"
	};

	let index : number = 2;

	while (index < process.argv.length && process.argv.at(index)!.at(0) === '-')
	{
		let arg = process.argv.at(index)!;

		if (arg.at(1) === undefined)
			break;

		let i = 1;
		while (arg.at(i) === '-')
			i++;

		if (arg.at(i) === 'r')
			command.recursive = true;
		else if (arg.at(i) === 'l')
		{
			if (command.recursive === false)
			{
				console.error("./spider: cannot use -l if -r isn't selected earlier");
				return undefined;
			}
			if (process.argv.at(index + 1) === undefined)
			{
				console.error("./spider: -l option needs an argument (./spider -r -l [N] URL)");
				return undefined;
			}
			if (Number.isNaN(Number(process.argv.at(index + 1))))
			{
				console.error("./spider: -l option's argument must be a number (./spider -r -l [N] URL)");
				return undefined;
			}
			command.level = Number(process.argv.at(index + 1));
			index++;
		}
		else if (arg.at(i) === 'p')
		{
			if (process.argv.at(index + 1) === undefined)
			{
				console.error("./spider: -p option needs an argument (./spider -p [PATH] URL)");
				return undefined;
			}
			command.path = process.argv.at(index + 1)!;
			index++;
		}	
		index++;
	}

	if (index !== process.argv.length - 1) {
		console.error("Usage: ./spider [-rlp] URL");
		return undefined;
	}

	command.url = process.argv.at(index)!;
	return command;
}

function getPath(url: URL, path: string): string
{
	if (/^https?:\/\//.test(path))
		return path;

	else if (/^\/\//.test(path))
		return url.protocol + path;

	else if (/^\//.test(path))
		return url.origin + path;

	if (url.href.at(url.href.length - 1) !== '/')
		return url.href + '/' + path;
	else
	return url.href + path;
}

function getFileName(url : URL) : string
{
	let index = url.pathname.length - 1;
	while (url.pathname[index] !== '/')
		index--;

	return url.pathname.substring(index);
}

async function fetchImage(url : URL, path : string)
{
	const response = await fetch(url);
	if (!response.ok)
		throw new Error(`${url.toString()}: error ${response.status}`);
	
	const buffer = await response.arrayBuffer();
	
	console.log(getFileName(url));
	fs.writeFileSync(path + getFileName(url), Buffer.from(buffer));
}

const imageVisited = new Set<string>();
async function scrapImage(url : URL, path : string)
{
	if (imageVisited.has(url.href))
		return;
	imageVisited.add(url.href);

	try 
	{
		try {
			await fetchImage(url, path);
		} catch (error) {
			if (url.protocol === 'https:') url.protocol = 'http:';
			else url.protocol = 'https:';

			await fetchImage(url, path);
		}
	} catch (error) {
		console.error("\x1b[35m" + error.message + "\x1b[0m");
	}
}

async function fecthHTML(url : URL, dest : string, level : number)
{
	const response = await fetch(url);
	if (!response.ok)
		throw new Error(`${url.toString()}: error ${response.status}`);
	
	const contentType = response.headers.get('content-type');
	if (contentType?.slice(0, 'text/html'.length) === 'text/html')
	{
		const text = await response.text();

		{	// html scrapping
			const regex = /<(a|iframe|link)\b[^>]*(?:href|src)=["']([^"']+\.html)["']/gi;

			let match = regex.exec(text); 
			while (match !== null)
			{
				await scrapHTML(new URL(getPath(url, String(match[2]))), dest, level);
				match = regex.exec(text);
			}
		}
		{	// images scrapping
			console.log(`\x1b[33mScrapping images of ${url.toString()}\x1b[0m`);
			const regex = /\b(?:src|href)=["']((?![^"']*File:)[^"']+\.(?:png|gif|jpg|jpeg|bmp))["']/gi;
			
			let match = regex.exec(text); 
			while (match !== null)
			{
				await scrapImage(new URL(getPath(url, String(match[1]))), dest);
				match = regex.exec(text);
			}
		}
	}
}
	
const HTMLVisited = new Set<string>();
async function scrapHTML(url : URL, dest : string, level : number)
{
	if (level === 0 || HTMLVisited.has(url.href))
		return;
	level--;
	HTMLVisited.add(url.href);
	
	try {
		try {
			await fecthHTML(url, dest, level);
		} catch (error) {
			if (url.protocol === 'https:') url.protocol = 'http:';
			else url.protocol = 'https:';

			await fecthHTML(url, dest, level);
		}
	} catch (error) {
		console.error("\x1b[31m" + error.message + "\x1b[0m");
	}
}

async function spider()
{
	let command : SpiderCommand | undefined = getSpiderCommand();
	if (command === undefined)
		return ;

	if (command.recursive === false)
		command.level = 1;

	if (!fs.existsSync(command.path))
	{
		try {
			fs.mkdirSync(command.path);
		}
		catch (err) {
			console.error(`./spider: ${command.path} doesn't exist and can't be created`);
		}
	}

	await scrapHTML(new URL(command.url), command.path, command.level);
}

spider();
