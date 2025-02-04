import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pathlib

sns.set_style("whitegrid")
fontsize = 16
legend_fontsize = 14

DATASET_PATH: pathlib.Path = pathlib.Path("../datasets/application_dataset.csv")
OUTPUT_BASE: pathlib.Path = pathlib.Path("../figures/")


def read_dataset():
    df = pd.read_csv(DATASET_PATH)

    df["created_at"] = pd.to_datetime(df["created_at"])
    df["year"] = df["created_at"].dt.year
    return df


def language_trends(df: pd.DataFrame):
    count_df = pd.DataFrame(index=df["year"].unique())

    for col, lang in zip(
        [
            "lan_Java",
            "lan_JavaScript",
            "lan_TypeScript",
            "lan_C#",
            "lan_Go",
            "lan_Python",
            "has_OtherLang",
        ],
        ["Java", "JavaScript", "TypeScript", "C#", "Go", "Python", "Other"],
    ):
        count_df[lang] = df.groupby("year")[col].apply(lambda x: (x > 0).sum())

    total_entries_per_year = df.groupby("year").size()

    count_df = count_df.div(total_entries_per_year, axis=0)

    count_df = count_df.loc[
        [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024], :
    ]

    plt.figure(figsize=(10, 6))

    sns.lineplot(data=count_df)

    plt.legend(fontsize=legend_fontsize)

    plt.xlabel("Year", fontsize=fontsize)

    plt.ylabel("Perc. of Repositories", fontsize=fontsize)

    plt.savefig(OUTPUT_BASE.joinpath("language_trends.pdf"), bbox_inches="tight")


def component_dist(df: pd.DataFrame):
    count_df = pd.DataFrame(index=range(0, 34))

    for col, ser in zip(
        ["num_ms", "num_sup_comp", "num_total_comp"],
        ["Microservices", "Supporting Components", "All Components"],
    ):
        count_df[ser] = df.groupby(col)[col].apply(lambda x: (x > 0).sum())

    count_df["Microservices_cdf"] = (
        count_df["Microservices"].cumsum() / count_df["Microservices"].sum()
    )
    count_df["Supporting_Components_cdf"] = (
        count_df["Supporting Components"].cumsum()
        / count_df["Supporting Components"].sum()
    )
    count_df["All_Components_cdf"] = (
        count_df["All Components"].cumsum() / count_df["All Components"].sum()
    )

    plt.figure(figsize=(10, 6))

    sns.lineplot(
        x=count_df.index,
        y=count_df["Microservices_cdf"],
        data=count_df,
        label="Microservices",
    )
    sns.lineplot(
        x=count_df.index,
        y=count_df["Supporting_Components_cdf"],
        data=count_df,
        label="Supporting Components",
    )
    sns.lineplot(
        x=count_df.index,
        y=count_df["All_Components_cdf"],
        data=count_df,
        label="All Components",
    )

    plt.legend(fontsize=legend_fontsize)

    plt.xlabel("No. of Components", fontsize=fontsize)

    plt.ylabel("Cum. Dist. of Repositories", fontsize=fontsize)

    plt.savefig(
        OUTPUT_BASE.joinpath("component_distribution_cdf.pdf"), bbox_inches="tight"
    )


def language_usage(df: pd.DataFrame):
    language_counts = pd.DataFrame(columns=["Language", "Count"])

    for col, lang in zip(
        [
            "lan_Java",
            "lan_JavaScript",
            "lan_TypeScript",
            "lan_C#",
            "lan_Python",
            "lan_Go",
            "has_OtherLang",
        ],
        ["Java", "JavaScript", "TypeScript", "C#", "Python", "Go", "Other"],
    ):
        count = (df[col] > 0).sum()
        language_counts = pd.concat(
            [language_counts, pd.DataFrame({"Language": [lang], "Count": [count]})]
        )

    plt.figure(figsize=(10, 6))

    ax = sns.barplot(x="Language", y="Count", data=language_counts)

    for label in ax.xaxis.get_ticklabels():
        label.set_fontsize(legend_fontsize)
    for label in ax.yaxis.get_ticklabels():
        label.set_fontsize(legend_fontsize)

    plt.xlabel("Language", fontsize=fontsize)

    plt.ylabel("No. of Repositories", fontsize=fontsize)

    plt.savefig(OUTPUT_BASE.joinpath("language_distribution.pdf"), bbox_inches="tight")


def categories_dist(df: pd.DataFrame):
    category_counts = pd.DataFrame(columns=["category", "Count"])

    for col, ser in zip(
        [
            "has_Datastorage",
            "has_MessageQueue",
            "has_Observability",
            "has_Gateway",
            "has_Frontend",
            "has_Communication",
            "has_Auth",
            "has_BenchmarkTooling",
            "has_OtherTech",
        ],
        [
            "Data\nStorage",
            "Message\nQueue",
            "Observability",
            "Gateway",
            "Frontend",
            "Communication",
            "Authentication",
            "Benchmark\nTooling",
            "Other",
        ],
    ):
        count = (df[col] > 0).sum() / len(df)
        category_counts = pd.concat(
            [category_counts, pd.DataFrame({"category": [ser], "Count": [count]})]
        )

    plt.figure(figsize=(10, 6))

    ax = sns.barplot(x="category", y="Count", data=category_counts)

    for label in ax.xaxis.get_ticklabels():
        label.set_fontsize(legend_fontsize)
    for label in ax.yaxis.get_ticklabels():
        label.set_fontsize(legend_fontsize)

    plt.xlabel("Category", fontsize=fontsize)

    plt.ylabel("Percentage of Repositories", fontsize=fontsize)

    plt.xticks(rotation=90)

    plt.savefig(OUTPUT_BASE.joinpath("category_distribution.pdf"), bbox_inches="tight")


def heatmap_by_lang(df: pd.DataFrame):
    heatmap_df = df[
        [
            "lan_Java",
            "lan_JavaScript",
            "lan_TypeScript",
            "lan_C#",
            "lan_Go",
            "lan_Python",
            "has_OtherLang",
            "tech_Prometheus",
            "tech_MongoDB",
            "tech_MySQL",
            "tech_PostgreSQL",
            "tech_MsSQL",
            "tech_Redis",
            "tech_React",
            "tech_NextJS",
            "tech_VueJS",
            "tech_AngularJS",
            "tech_Jaeger",
            "tech_Zipkin",
            "tech_OpenTelemetry",
            "tech_ElasticSearch",
            "tech_Kafka",
            "tech_RabbitMQ",
            "tech_Consul",
            "tech_nginx",
            "tech_Zuul",
        ]
    ].copy()

    heatmap_df.columns = [
        "Java",
        "JavaScript",
        "TypeScript",
        "C#",
        "Go",
        "Python",
        "Other",
        "Prometheus",
        "MongoDB",
        "MySQL",
        "PostgreSQL",
        "MsSQL",
        "Redis",
        "React",
        "NextJS",
        "VueJS",
        "AngularJS",
        "Jaeger",
        "Zipkin",
        "OpenTelemetry",
        "ElasticSearch",
        "Kafka",
        "RabbitMQ",
        "Consul",
        "nginx",
        "Zuul",
    ]

    languages = ["Java", "JavaScript", "C#", "TypeScript", "Go", "Python", "Other"]
    services = [
        "Prometheus",
        "MongoDB",
        "MySQL",
        "PostgreSQL",
        "MsSQL",
        "Redis",
        "React",
        "NextJS",
        "VueJS",
        "AngularJS",
        "Jaeger",
        "Zipkin",
        "OpenTelemetry",
        "ElasticSearch",
        "Kafka",
        "RabbitMQ",
        "Consul",
        "nginx",
        "Zuul",
    ]

    count_dict = {lan: {ser: 0.0 for ser in services} for lan in languages}

    for lan in languages:
        for ser in services:
            count_dict[lan][ser] = round(
                (sum((heatmap_df[lan] > 0) & (heatmap_df[ser] > 0)))
                / sum(heatmap_df[lan] > 0),
                2,
            )

    count_df = pd.DataFrame.from_dict(count_dict, orient="index")

    plt.figure(figsize=(10, 6))

    ax = sns.heatmap(
        count_df.T,
        annot=True,
        cmap="coolwarm",
        fmt="",
        annot_kws={"size": legend_fontsize},
    )
    for label in ax.xaxis.get_ticklabels():
        label.set_fontsize(legend_fontsize)
    for label in ax.yaxis.get_ticklabels():
        label.set_fontsize(legend_fontsize)
    plt.xlabel("Languages", fontsize=fontsize)
    plt.ylabel("Supporting Components", fontsize=16)
    plt.savefig(
        OUTPUT_BASE.joinpath("component_heatmap_by_language.pdf"), bbox_inches="tight"
    )


def heatmap_by_tech(df: pd.DataFrame):
    heatmap_df = df[
        [
            "lan_Java",
            "lan_JavaScript",
            "lan_TypeScript",
            "lan_C#",
            "lan_Go",
            "lan_Python",
            "has_OtherLang",
            "tech_Prometheus",
            "tech_MongoDB",
            "tech_MySQL",
            "tech_PostgreSQL",
            "tech_MsSQL",
            "tech_Redis",
            "tech_React",
            "tech_NextJS",
            "tech_VueJS",
            "tech_AngularJS",
            "tech_Jaeger",
            "tech_Zipkin",
            "tech_OpenTelemetry",
            "tech_ElasticSearch",
            "tech_Kafka",
            "tech_RabbitMQ",
            "tech_Consul",
            "tech_nginx",
            "tech_Zuul",
        ]
    ].copy()

    heatmap_df.columns = [
        "Java",
        "JavaScript",
        "TypeScript",
        "C#",
        "Go",
        "Python",
        "Other",
        "Prometheus",
        "MongoDB",
        "MySQL",
        "PostgreSQL",
        "MsSQL",
        "Redis",
        "React",
        "NextJS",
        "VueJS",
        "AngularJS",
        "Jaeger",
        "Zipkin",
        "OpenTelemetry",
        "ElasticSearch",
        "Kafka",
        "RabbitMQ",
        "Consul",
        "nginx",
        "Zuul",
    ]

    languages = ["Java", "JavaScript", "C#", "TypeScript", "Go", "Python", "Other"]
    services = [
        "Prometheus",
        "MongoDB",
        "MySQL",
        "PostgreSQL",
        "MsSQL",
        "Redis",
        "React",
        "NextJS",
        "VueJS",
        "AngularJS",
        "Jaeger",
        "Zipkin",
        "OpenTelemetry",
        "ElasticSearch",
        "Kafka",
        "RabbitMQ",
        "Consul",
        "nginx",
        "Zuul",
    ]

    # count_dict = {lan: {ser: 0 for ser in services} for lan in languages}
    count_dict = {ser: {lan: 0.0 for lan in languages} for ser in services}

    for ser in services:
        for lan in languages:
            # count_dict[lan][ser] = round((sum((heatmap_df[lan] > 0) & (heatmap_df[ser] > 0))) / sum(heatmap_df[ser] > 0), 2)
            count_dict[ser][lan] = round(
                (sum((heatmap_df[lan] > 0) & (heatmap_df[ser] > 0)))
                / sum(heatmap_df[ser] > 0),
                2,
            )

    count_df = pd.DataFrame.from_dict(count_dict, orient="index")

    plt.figure(figsize=(10, 6))
    ax = sns.heatmap(
        count_df.T, annot=True, cmap="coolwarm", fmt="", annot_kws={"size": 12}
    )
    for label in ax.xaxis.get_ticklabels():
        label.set_fontsize(legend_fontsize)
    for label in ax.yaxis.get_ticklabels():
        label.set_fontsize(legend_fontsize)
    # plt.xlabel("Languages", fontsize=fontsize)
    plt.xlabel("Supporting Components", fontsize=fontsize)
    # plt.ylabel("Supporting Components", fontsize=fontsize)
    plt.ylabel("Languages", fontsize=fontsize)
    plt.savefig(
        OUTPUT_BASE.joinpath("component_heatmap_by_tech.pdf"), bbox_inches="tight"
    )


def gateway_usage(df: pd.DataFrame):
    gateway_counts = pd.DataFrame(columns=["Gateway", "Count"])

    for col, lang in zip(
        [
            "tech_nginx",
            "tech_Zuul",
            "tech_Ocelot",
            "tech_Envoy",
            "tech_Kong",
            "tech_Traefik",
        ],
        ["nginx", "Zuul", "Ocelot", "Envoy", "Kong", "Traefik"],
    ):
        count = (df[col] > 0).sum()
        gateway_counts = pd.concat(
            [gateway_counts, pd.DataFrame({"Gateway": [lang], "Count": [count]})]
        )

    plt.figure(figsize=(10, 6))

    ax = sns.barplot(x="Gateway", y="Count", data=gateway_counts)

    for label in ax.xaxis.get_ticklabels():
        label.set_fontsize(legend_fontsize)
    for label in ax.yaxis.get_ticklabels():
        label.set_fontsize(legend_fontsize)

    plt.xlabel("Gateway", fontsize=fontsize)

    plt.ylabel("No. of Repositories", fontsize=fontsize)

    plt.savefig(OUTPUT_BASE.joinpath("gateway_distribution.pdf"), bbox_inches="tight")


def database_usage(df: pd.DataFrame):
    database_counts = pd.DataFrame(columns=["Database", "Count"])

    for col, lang in zip(
        [
            "tech_MongoDB",
            "tech_Redis",
            "tech_PostgreSQL",
            "tech_MySQL",
            "tech_MsSQL",
            "tech_MariaDB",
            "tech_SnowflakeDB",
            "tech_Cassandra",
            "tech_OracleDB",
            "tech_Database",
        ],
        [
            "MongoDB",
            "Redis",
            "PostgreSQL",
            "MySQL",
            "MsSQL",
            "MariaDB",
            "SnowflakeDB",
            "Cassandra",
            "OracleDB",
            "Other",
        ],
    ):
        count = (df[col] > 0).sum()
        database_counts = pd.concat(
            [database_counts, pd.DataFrame({"Database": [lang], "Count": [count]})]
        )

    plt.figure(figsize=(10, 6))

    ax = sns.barplot(x="Database", y="Count", data=database_counts)

    for label in ax.xaxis.get_ticklabels():
        label.set_fontsize(legend_fontsize)
    for label in ax.yaxis.get_ticklabels():
        label.set_fontsize(legend_fontsize)

    plt.xlabel("Database", fontsize=fontsize)

    plt.xticks(rotation=90)

    plt.ylabel("No. of Repositories", fontsize=fontsize)

    plt.savefig(OUTPUT_BASE.joinpath("database_distribution.pdf"), bbox_inches="tight")


def main():
    df = read_dataset()

    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)

    language_usage(df)
    language_trends(df)
    component_dist(df)
    categories_dist(df)
    database_usage(df)
    gateway_usage(df)
    heatmap_by_lang(df)
    heatmap_by_tech(df)


if __name__ == "__main__":
    main()
