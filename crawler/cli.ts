function printUsage() {
	console.error("Usage:\n\tdeno run search:{applications|workloads}");
	console.error(
		"\tQuery the official GitHub REST API for microservice applications or workloads.",
	);
}

export function parseSearchArgs(): "applications" | "workloads" {
	if (Deno.args.length !== 1) {
		console.error("Missing one positional argument");
		printUsage();
		Deno.exit(1);
	}
	switch (Deno.args[0]) {
		case "applications":
			return "applications";
		case "workloads":
			return "workloads";
		default:
			printUsage();
			Deno.exit(1);
	}
}

export function parseCodeArgs(): "technologies" | "containerization" {
	if (Deno.args.length !== 1) {
		console.error("Missing one positional argument");
		printUsage();
		Deno.exit(1);
	}
	switch (Deno.args[0]) {
		case "technologies":
			return "technologies";
		case "containerization":
			return "containerization";
		default:
			printUsage();
			Deno.exit(1);
	}
}
