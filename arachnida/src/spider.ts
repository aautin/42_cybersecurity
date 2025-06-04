import fetch from "node-fetch";

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

async function spider()
{
	let command : SpiderCommand | undefined = getSpiderCommand();
	if (command === undefined)
		return ;

	if (command.recursive === false)
		command.level = 1;

	await scrap(new URL(command.url), command.path, command.level);
}

function getPath(url : URL, path : string) : string
{
	if (/^https?:\/\//.test(path))
		return path;

	else if (/^\/\//.test(path))
    	return url.protocol + path;

	else if (/^\//.test(path))
   		return url.origin + '/' + path;

	if (url.href.at(url.href.length - 1) !== '/')
		return url.href + '/' + path;
	else 
		return url.href + path;
}

async function scrap(url : URL, path : string, level : number)
{
	if (level === 0)
		return;

	try {
		const response = await fetch(url);
		if (!response.ok)
			throw new Error(`Response status: ${response.status}`);

		
		const contentType = response.headers.get('content-type');
		if (contentType?.slice(0, 'text/html'.length) === 'text/html')
		{
			const text = await response.text();
			const regex = /\b(?:src|href)=["']([^"']+\.(?:png|gif|jpg|jpeg|bmp))["']/gi;

			let match = regex.exec(text); 
			while (match !== null)
			{
				let path = getPath(url, String(match[1]));
				console.log(path);
				match = regex.exec(text);
			}
		}
	} catch (error) {
		console.error(error.message);
	}
}

spider();
