import { writeJson } from "https://deno.land/x/jsonfile@1.0.0/mod.ts";

export async function writeFilePretty(path: string, data: object) {
	try {
		await writeJson(path, data, { spaces: 2 });
	} catch (e) {
		console.error(e);
	}
}
