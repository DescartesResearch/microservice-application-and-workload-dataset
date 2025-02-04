import { Octokit } from "https://esm.sh/octokit@4.0.3?dts";
import { parse } from "@std/csv/parse";
import * as path from "jsr:@std/path";
import { writeFilePretty } from "./write.ts";
import { parseCodeArgs } from "./cli.ts";
import {
	COMPONENTS_FILE_PATH,
	CONTAINERIZATION_OUTPUT_BASE,
	TECHNOLOGIES_OUTPUT_BASE,
} from "./constants.ts";

const TECHNOLOGY_QUERY_TERMS = {
	Prometheus: "prometheus in:file,path",
	MongoDB: "mongo in:file,path NOT language:json",
	MySQL: "mysql in:file,path",
	OracleDB: "oracledb in:file,path",
	SnowflakeDB: "snowflake in:file,path",
	PostgreSQL: "postgresql in:file,path",
	MsSQL: "mssql in:file,path",
	Redis: "redis in:file,path NOT filename:license",
	Cassandra: "cassandra in:file,path",
	MariaDB: "mariadb in:file,path",
	Database: "database in:file,path",
	MinIO: "minio in:file,path",
	React: "react in:file filename:package extension:json",
	NextJS: "next in:file filename:package extension:json",
	Svelte: "svelte in:file filename:package extension:json",
	SvelteKit: "sveltejs/kit in:file filename:package extension:json",
	VueJS: "vue in:file filename:package extension:json",
	Nuxt: "nuxt in:file filename:package extension:json",
	AngularJS: "angular in:file filename:package extension:json",
	AnalogJS: "analogjs in:file filename:package extension:json",
	Jaeger: "jaeger in:file,path",
	Zipkin: "zipkin in:file,path",
	OpenTelemetry: "otel in:file,path",
	Logstash: "logstash in:file,path",
	Filebeat: "filebeat in:file,path",
	ElasticSearch: "elasticsearch in:file,path",
	Kafka: "kafka in:file,path",
	RabbitMQ: "rabbitmq in:file,path",
	Nats: "nats in:file,path",
	Dapr: "dapr in:file,path",
	Consul: "consul in:file,path",
	Istio: "istio in:file,path",
	nginx: "nginx in:file,path",
	Zuul: "zuul in:file,path",
	Kong: "kong in:file,path NOT language:json",
	Envoy: "envoy in:file,path",
	Traefik: "traefik in:file,path",
	Ocelot: "ocelot in:file,path",
	Zookeeper: "zookeeper in:file,path",
	Hystrix: "hystrix in:file,path",
	Kiali: "kiali in:file,path",
	Grafana: "grafana in:file,path",
	Kibana: "kibana in:file,path",
	Akhq: "akhq in:file,path",
	Portainer: "portainer in:file,path",
	Keycloak: "keycloak in:file,path",
	Vault: "vault in:file,path",
	Eureka: "eureka in:file,path",
	Locust: "locust in:file language:python",
	K6: '"k6" in:file language:javascript',
	JMeter: "jmeter in:file extension:jmx",
};

const CONTAINERIZATION_QUERY_TERMS = {
	Dockerfile: "Dockerfile in:path",
	DockerCompose: "docker-compose in:path language:yaml",
	Kubernetes: '"kind: " in:file language:yaml',
};

function newApiClient(token: string) {
	return new Octokit({ auth: token });
}

async function searchCode(
	client: Octokit,
	repo: string,
	queryTerms: { [key: string]: string },
	base: string,
) {
	console.log(`Querying ${repo}`);
	const out: { [key: string]: unknown } = {};
	for (const [key, query] of Object.entries(queryTerms)) {
		const q = `repo:${repo} ${query}`;
		const response = await client.request(
			`GET /search/code?q=${encodeURIComponent(q)}`,
		);
		const data = response.data;
		out[key] = data;
	}
	await writeFilePretty(
		path.join(base, `${repo.replaceAll("/", "---")}.json`),
		out,
	);
}

async function main() {
	const flag = parseCodeArgs();
	const queryTerms =
		flag === "technologies"
			? TECHNOLOGY_QUERY_TERMS
			: CONTAINERIZATION_QUERY_TERMS;
	const base =
		flag === "technologies"
			? TECHNOLOGIES_OUTPUT_BASE
			: CONTAINERIZATION_OUTPUT_BASE;
	const token = Deno.env.get("GITHUB_API_TOKEN");
	if (token === undefined) {
		console.error("Missing GitHub API token! Exiting...");
		Deno.exit(1);
	}
	await Deno.mkdir(base, { recursive: true });
	const client = newApiClient(token);

	const text = await Deno.readTextFile(COMPONENTS_FILE_PATH);

	const data = parse(text, { columns: ["url", "num_ms", "num_sup_comp"] });
	const urls = data.map((e) => e.url);

	for (const url of urls) {
		if (url === "") continue;
		const components = url.split("/");
		const repo = `${components[components.length - 2]}/${components[components.length - 1]}`;
		await searchCode(client, repo, queryTerms, base);
	}

	// See: https://github.com/octokit/octokit.js/issues/2079
	Deno.exit(0);
}

if (import.meta.main) {
	main();
}
