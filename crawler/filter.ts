import { parseArgs } from "./cli.ts";
import {
	APPLICATION_AUTOMATIC_FILTERING,
	APPLICATION_OUTPUT_BASE,
	APPLICATION_SPREADSHEET_IMPORT,
	WORKLOAD_AUTOMATIC_FILTERING,
	WORKLOAD_OUTPUT_BASE,
	WORKLOAD_SPREADSHEET_IMPORT,
} from "./constants.ts";
import { loadJson } from "./load.ts";
import { type RepoSearchResult } from "./schema.ts";
import { writeFilePretty } from "./write.ts";
import * as path from "jsr:@std/path";

const POPULARITY_THRESHHOLD: number = 5;

async function main() {
	const filtered: RepoSearchResult = [];
	const seen: Set<string> = new Set();
	let total = 0;
	const flag = parseArgs();
	const base =
		flag === "applications" ? APPLICATION_OUTPUT_BASE : WORKLOAD_OUTPUT_BASE;
	const outJson =
		flag === "applications"
			? APPLICATION_AUTOMATIC_FILTERING
			: WORKLOAD_AUTOMATIC_FILTERING;
	const outSpreadsheet =
		flag === "applications"
			? APPLICATION_SPREADSHEET_IMPORT
			: WORKLOAD_SPREADSHEET_IMPORT;
	for await (const entry of Deno.readDir(base)) {
		if (entry.isDirectory) {
			const dirPath = path.join(base, entry.name);
			for await (const entry of Deno.readDir(dirPath)) {
				if (isJsonFile(entry)) {
					const filePath = path.join(dirPath, entry.name);
					total += await processJson(filePath, filtered, seen);
				}
			}
		}
	}
	console.log(`Processed ${total} number of API results`);
	console.log(`Writing ${filtered.length} entries to ${outJson}`);
	await writeFilePretty(outJson, filtered);
	await Deno.writeTextFile(
		outSpreadsheet,
		filtered.reduce((ack, curr) => `${ack}\n${curr.html_url}`, ""),
	);
}

async function processJson(
	path: string,
	out: RepoSearchResult,
	seen: Set<string>,
) {
	const data = await loadJson(path);

	if (!data.success || data.data === undefined) {
		console.error(`failed to load ${path}: ${data.error}`);
	} else {
		const arr = data.data;
		out.push(
			...arr.filter((e) => {
				const isDuplicate = seen.has(e.html_url);
				seen.add(e.html_url);
				const check =
					e.language !== null &&
					!isDuplicate &&
					!e.is_template &&
					!e.fork &&
					(e.stargazers_count >= POPULARITY_THRESHHOLD ||
						e.forks_count >= POPULARITY_THRESHHOLD);
				return check;
			}),
		);
		return arr.length;
	}

	return 0;
}

function isJsonFile(entry: Deno.DirEntry): boolean {
	return entry.isFile && entry.name.endsWith(".json");
}

if (import.meta.main) {
	main();
}
