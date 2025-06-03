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
		path : ""
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

function spider() : void
{
	let command : SpiderCommand | undefined = getSpiderCommand();
	if (command === undefined)
		return ;
	console.log(command);
	return ;
}

spider();
