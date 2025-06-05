import * as fs from  'fs/promises';
import exifr from 'exifr';


async function scorpion() {
	let filenames = process.argv.slice(2);

	while (filenames.length) {
		let file: string = filenames.pop()!;

		try {
			// Check file stats
			const stats = await fs.stat(file);
			console.log(stats);

			// Optionally filter JPEG files by extension
			if (/\.jpe?g$/i.test(file)) {
				const exifr_content = await exifr.parse(file);
				if (exifr_content)
					console.log('EXIF data:', exifr_content);
			}
		} catch (error: any) {
			console.error(`\x1b[31m${error.message}\x1b[0m`);
		}
	}
}

scorpion();
