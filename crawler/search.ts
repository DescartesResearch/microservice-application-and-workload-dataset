import { Octokit } from "https://esm.sh/octokit@4.0.3?dts";
import { format } from "@std/datetime";
import * as path from "jsr:@std/path";
import { APPLICATION_OUTPUT_BASE, WORKLOAD_OUTPUT_BASE } from "./constants.ts";
import { writeFilePretty } from "./write.ts";
import { parseArgs } from "./cli.ts";

const APPLICATION_QUERY_TERMS = [
	"microservice application",
	"micro-service application",
	"micro service application",
	"microservice system",
	"micro-service system",
	"micro service system",
];

const WORKLOAD_QUERY_TERMS = [
	"workload trace",
	'"cluster data"',
	'"cluster-data"',
	'"trace data"',
	'"trace-data"',
	'"microservice workload"',
	'"micro-service workload"',
	'"micro service workload"',
	'"serverless workload"',
	'"cloud workload"',
	'"cloud dataset"',
	'"cloud data-set"',
	'"cloud data set"',
	'"cluster trace"',
	'"cluster-trace"',
	'"tracing data"',
];

Date.prototype.addDays = function (days: number) {
	const date = new Date(this.valueOf());
	date.setDate(date.getDate() + days);
	return date;
};

const START_DATE = new Date("2020-01-01");
const END_DATE = new Date("2025-01-15");

async function searchRepositories(
	client: Octokit,
	keyword: string,
	timeSlice: string,
	out: string,
) {
	const dirPath = await mkOutputDir(out, keyword.replaceAll(" ", "_"));
	const iterator = newRequestIterator(client, keyword, timeSlice);
	const time = timeSlice.replaceAll("..", "--");
	let page = 1;
	for await (const { data: repositories } of iterator) {
		const fileName = `${time}-page-${page}.json`;
		console.log(
			`Saving page ${page} for keyword ${keyword} and time slice ${time}`,
		);
		await writeFilePretty(path.join(dirPath, fileName), repositories);
		page++;
	}
}

function newApiClient(token: string) {
	return new Octokit({ auth: token });
}

function newRequestIterator(
	client: Octokit,
	search: string,
	timeSlice: string,
) {
	return client.paginate.iterator(
		`GET /search/repositories?q=${encodeURIComponent(
			`${search} in:readme|name|description pushed:${timeSlice} is:public archived:false`,
		)}`,
	);
}

async function mkOutputDir(base: string, dirName: string) {
	const dirPath = path.join(base, dirName);
	await Deno.mkdir(dirPath, { recursive: true });
	return dirPath;
}

async function main() {
	const flag = parseArgs();

	const queryTerms =
		flag === "applications" ? APPLICATION_QUERY_TERMS : WORKLOAD_QUERY_TERMS;
	const out =
		flag === "applications" ? APPLICATION_OUTPUT_BASE : WORKLOAD_OUTPUT_BASE;

	const token = Deno.env.get("GITHUB_API_TOKEN");
	if (token === undefined) {
		console.error("Missing GitHub API token! Exiting...");
		Deno.exit(1);
	}
	const client = newApiClient(token);
	for (const keyword of queryTerms) {
		let current = START_DATE;
		let next = current.addDays(1);
		while (current < END_DATE) {
			const currentFmt = format(current, "yyyy-MM-dd");
			const nextFmt = format(next, "yyyy-MM-dd");
			await searchRepositories(
				client,
				keyword,
				`${currentFmt}..${nextFmt}`,
				out,
			);
			current = next;
			next = next.addDays(1);
		}
	}

	// See: https://github.com/octokit/octokit.js/issues/2079
	Deno.exit(0);
}

if (import.meta.main) {
	main();
}
