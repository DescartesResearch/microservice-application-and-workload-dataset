import pandas as pd
import pathlib
import json

API_DATA_PATH: pathlib.Path = pathlib.Path(
    "../raw_data/applications/automatic_filtering.json"
)
COMP_DATA_PATH: pathlib.Path = pathlib.Path("../raw_data/application_components.csv")
TECHNOLOGIES_PATH: pathlib.Path = pathlib.Path("../raw_data/technologies/")
LANGUAGE_PATH: pathlib.Path = pathlib.Path("../raw_data/languages")
CONTAINERIZATION_PATH: pathlib.Path = pathlib.Path("../raw_data/containerization/")
GITHUB_URL_BASE: str = "https://github.com/"
OUT_BASE: pathlib.Path = pathlib.Path("../datasets")
OUT_PATH: pathlib.Path = OUT_BASE.joinpath("application_dataset.csv")


def read_component_count_csv(path: pathlib.Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep=",", names=["url", "num_ms", "num_sup_comp"]).set_index(
        "url", drop=True, verify_integrity=True
    )
    df["num_total_comp"] = df["num_ms"] + df["num_sup_comp"]

    # Sanity checks
    assert df["num_ms"].min() > 0, "found entry with zero microservices"
    assert df["num_total_comp"].min() > 0, "found entry with zero total components"
    assert df["num_total_comp"].max() == 33, "invalid known maximum of total components"
    assert df["num_sup_comp"].max() == 21, (
        "invalid known maximum of supporting components"
    )
    assert df["num_ms"].max() == 14, "invalid known maximum of microservices"
    assert len(df) == 553, f"invalid number of entries: {len(df)}"
    assert not (df.isna().values.any()), "missing values in table"

    return df


def read_technologies_jsons(path: pathlib.Path) -> pd.DataFrame:
    data = []
    for file in path.glob("*.json"):
        entry = {}
        assert file.is_file()
        full_name = file.name.replace("---", "/", 1).removesuffix(".json")
        entry["url"] = f"{GITHUB_URL_BASE}{full_name}"
        with file.open() as f:
            obj = json.load(f)
        assert isinstance(obj, dict)
        for key, value in obj.items():
            entry[key] = value["total_count"]
        for key in [
            "MongoDB",
            "MySQL",
            "OracleDB",
            "SnowflakeDB",
            "PostgreSQL",
            "MsSQL",
            "Redis",
            "Cassandra",
            "MariaDB",
        ]:
            if entry[key] > 0:
                entry["Database"] = 0
                break
        data.append(entry)

    df = pd.DataFrame(data)

    # Sanity Checks
    assert len(df) == 553, f"invalid number of entries: {len(df)}"

    return df.set_index("url", drop=True, verify_integrity=True)


def read_language_jsons(path: pathlib.Path) -> pd.DataFrame:
    data = []
    for file in path.glob("*.json"):
        entry = {}
        full_name = file.name.replace("---", "/", 1).removesuffix(".json")
        entry["url"] = f"{GITHUB_URL_BASE}{full_name}"
        with file.open() as f:
            obj = json.load(f)
        assert isinstance(obj, dict)

        for key, value in obj.items():
            entry[key] = float(value["percentage"])
        data.append(entry)

    df = (
        pd.DataFrame(data)
        .set_index("url", drop=True, verify_integrity=True)
        .fillna(value=0.0)
    )
    df = df.drop(
        columns=[
            "HTML",
            "CSS",
            "Dockerfile",
            "Smarty",
            "Shell",
            "HCL",
            "Makefile",
            "PLpgSQL",
            "PowerShell",
            "Jupyter Notebook",
            "SCSS",
            "Less",
            "TSQL",
            "Mustache",
            "Handlebars",
            "Batchfile",
            "FreeMarker",
            "Gherkin",
            "TeX",
            "JSON",
            "YAML",
            "Procfile",
            "Mako",
            "Inno Setup",
            "MDX",
            "CMake",
            "XSLT",
            "Pug",
            "EJS",
            "Starlark",
            "Thrift",
            "ASL",
            "Sass",
            "Nunjucks",
            "Stylus",
            "Bicep",
            "RAML",
            "Open Policy Agent",
        ]
    )

    # Aggregate Languages
    df["JavaScript"] = df["JavaScript"] + df["Vue"] + df["Svelte"]
    df = df.drop(columns=["Vue", "Svelte"])
    df["Python"] = df["Python"] + df["Cython"]
    df = df.drop(columns=["Cython"])
    df["C#"] = df["C#"] + df["ASP.NET"]
    df = df.drop(columns=["ASP.NET"])

    for col in df.columns:
        df.loc[df[col] < 1.0, col] = 0.0

    # Drop languages with all zero usage
    df = df.loc[:, (df != 0.0).any(axis=0)]

    # Sanity Checks
    assert len(df) == 553, f"invalid number of entries: {len(df)}"
    assert (df.max() > 1.0).all(), "all language usage should be above 1%"
    return df


def read_containerization_jsons(path: pathlib.Path) -> pd.DataFrame:
    data = []
    for file in path.glob("*.json"):
        full_name = file.name.replace("---", "/", 1).removesuffix(".json")
        with file.open() as f:
            obj = json.load(f)
        assert isinstance(obj, dict)
        data.append(
            {
                "url": f"{GITHUB_URL_BASE}{full_name}",
                "docker": (obj["Dockerfile"]["total_count"] > 0),
                "compose": (obj["DockerCompose"]["total_count"] > 0),
                "kubernetes": (obj["Kubernetes"]["total_count"] > 0),
            }
        )

    df = pd.DataFrame(data).set_index("url", drop=True, verify_integrity=True)

    # Sanity Checks
    assert len(df) == 553, f"invalid number of entries: {len(df)}"

    return df


def report_docker_usage(df: pd.DataFrame):
    print(f"Docker Usage: {df['docker'].value_counts(normalize=True)}")
    print(f"Docker-Compose Usage: {df['compose'].value_counts(normalize=True)}")
    print(f"Kubernetes Usage: {df['kubernetes'].value_counts(normalize=True)}")


def aggregate():
    comp_df = read_component_count_csv(COMP_DATA_PATH)
    api_data = pd.read_json(API_DATA_PATH).set_index(
        "html_url", drop=True, verify_integrity=True
    )
    api_cols = {
        "fork": "is_fork",
        "forks": "num_forks",
        "watchers": "num_watchers",
        "archived": "is_archived",
    }
    api_data.rename(columns=api_cols, inplace=True)
    code_data = read_technologies_jsons(TECHNOLOGIES_PATH)
    code_cols = {col: f"tech_{col}" for col in code_data.columns}
    code_data.rename(columns=code_cols, inplace=True)
    docker_df = read_containerization_jsons(CONTAINERIZATION_PATH)
    language_df = read_language_jsons(LANGUAGE_PATH)
    lang_cols = {col: f"lan_{col}" for col in language_df.columns}
    language_df = language_df.rename(columns=lang_cols)

    df = (
        comp_df.join(api_data, how="inner", validate="1:1")
        .join(language_df, how="inner", validate="1:1")
        .join(code_data, how="inner", validate="1:1")
        .join(docker_df, how="inner", validate="1:1")
    )
    assert len(df) == 553, f"invalid number of entries: {len(df)}"

    df = df.loc[
        :,
        [
            "id",
            "created_at",
            "updated_at",
            "size",
            "language",
            "has_wiki",
            "license",
            "is_template",
            "num_ms",
            "num_sup_comp",
            "num_total_comp",
            *api_cols.values(),
            *lang_cols.values(),
            *code_cols.values(),
            "docker",
            "compose",
            "kubernetes",
        ],
    ]

    otherLangs = [col for col in lang_cols.values()]
    for lang in ["Java", "JavaScript", "TypeScript", "C#", "Go", "Python"]:
        otherLangs.remove(f"lan_{lang}")

    df["has_OtherLang"] = (df.loc[:, otherLangs] > 0).sum(axis=1)
    df["has_Gateway"] = (
        df.loc[
            :,
            [
                "tech_nginx",
                "tech_Zuul",
                "tech_Kong",
                "tech_Envoy",
                "tech_Traefik",
                "tech_Ocelot",
            ],
        ]
        > 0
    ).sum(axis=1)
    df["has_MessageQueue"] = (
        df.loc[
            :,
            [
                "tech_Kafka",
                "tech_RabbitMQ",
                "tech_Nats",
            ],
        ]
        > 0
    ).sum(axis=1)
    df["has_Auth"] = (
        df.loc[
            :,
            [
                "tech_Keycloak",
                "tech_Vault",
            ],
        ]
        > 0
    ).sum(axis=1)
    df["has_BenchmarkTooling"] = (
        df.loc[
            :,
            [
                "tech_Locust",
                "tech_K6",
                "tech_JMeter",
            ],
        ]
        > 0
    ).sum(axis=1)
    df["has_Datastorage"] = (
        df.loc[
            :,
            [
                "tech_MongoDB",
                "tech_MySQL",
                "tech_PostgreSQL",
                "tech_SnowflakeDB",
                "tech_OracleDB",
                "tech_MsSQL",
                "tech_Redis",
                "tech_Cassandra",
                "tech_MariaDB",
                "tech_ElasticSearch",
                "tech_MinIO",
                "tech_Database",
            ],
        ]
        > 0
    ).sum(axis=1)
    df["has_Observability"] = (
        df.loc[
            :,
            [
                "tech_Prometheus",
                "tech_Jaeger",
                "tech_Zipkin",
                "tech_OpenTelemetry",
                "tech_Logstash",
                "tech_Filebeat",
                "tech_Hystrix",
                "tech_Kiali",
                "tech_Grafana",
                "tech_Kibana",
                "tech_Akhq",
                "tech_Portainer",
            ],
        ]
        > 0
    ).sum(axis=1)
    df["has_Frontend"] = (
        df.loc[
            :,
            [
                "tech_React",
                "tech_NextJS",
                "tech_Svelte",
                "tech_SvelteKit",
                "tech_VueJS",
                "tech_Nuxt",
                "tech_AngularJS",
                "tech_AnalogJS",
            ],
        ]
        > 0
    ).sum(axis=1)
    df["has_Communication"] = (
        df.loc[
            :,
            [
                "tech_Dapr",
                "tech_Istio",
                "tech_Consul",
            ],
        ]
        > 0
    ).sum(axis=1)
    df["has_OtherTech"] = (
        df.loc[
            :,
            [
                "tech_Eureka",
                "tech_Zookeeper",
            ],
        ]
        > 0
    ).sum(axis=1)

    report_docker_usage(df)

    OUT_BASE.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)


if __name__ == "__main__":
    aggregate()
