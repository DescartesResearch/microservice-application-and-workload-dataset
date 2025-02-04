import { readJson } from "https://deno.land/x/jsonfile@1.0.0/mod.ts";
import { RepoSearchResult } from "./schema.ts";

export async function loadJson(path: string) {
	try {
		const data = await readJson(path);
		return { success: true, data: await RepoSearchResult.parseAsync(data) };
	} catch (err) {
		return { success: false, error: err };
	}
}
