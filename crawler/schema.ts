import { z } from "zod";

// Generated from `schema.json` using https://stefanterdell.github.io/json-schema-to-zod-react/
export const RepoSearchResult = z.array(
	z
		.object({
			id: z.number().int(),
			node_id: z.string(),
			name: z.string(),
			full_name: z.string(),
			owner: z.union([
				z.null(),
				z
					.object({
						name: z.union([z.string(), z.null()]).optional(),
						email: z.union([z.string(), z.null()]).optional(),
						login: z.string(),
						id: z.number().int(),
						node_id: z.string(),
						avatar_url: z.string().url(),
						gravatar_id: z.union([z.string(), z.null()]),
						url: z.string().url(),
						html_url: z.string().url(),
						followers_url: z.string().url(),
						following_url: z.string(),
						gists_url: z.string(),
						starred_url: z.string(),
						subscriptions_url: z.string().url(),
						organizations_url: z.string().url(),
						repos_url: z.string().url(),
						events_url: z.string(),
						received_events_url: z.string().url(),
						type: z.string(),
						site_admin: z.boolean(),
						starred_at: z.string().optional(),
						user_view_type: z.string().optional(),
					})
					.describe("A GitHub user."),
			]),
			private: z.boolean(),
			html_url: z.string().url(),
			description: z.union([z.string(), z.null()]),
			fork: z.boolean(),
			url: z.string().url(),
			created_at: z.string().datetime(),
			updated_at: z.string().datetime(),
			pushed_at: z.string().datetime(),
			homepage: z.union([z.string().url(), z.null(), z.string()]),
			size: z.number().int(),
			stargazers_count: z.number().int(),
			watchers_count: z.number().int(),
			language: z.union([z.string(), z.null()]),
			forks_count: z.number().int(),
			open_issues_count: z.number().int(),
			master_branch: z.string().optional(),
			default_branch: z.string(),
			score: z.number(),
			forks_url: z.string().url(),
			keys_url: z.string(),
			collaborators_url: z.string(),
			teams_url: z.string().url(),
			hooks_url: z.string().url(),
			issue_events_url: z.string(),
			events_url: z.string().url(),
			assignees_url: z.string(),
			branches_url: z.string(),
			tags_url: z.string().url(),
			blobs_url: z.string(),
			git_tags_url: z.string(),
			git_refs_url: z.string(),
			trees_url: z.string(),
			statuses_url: z.string(),
			languages_url: z.string().url(),
			stargazers_url: z.string().url(),
			contributors_url: z.string().url(),
			subscribers_url: z.string().url(),
			subscription_url: z.string().url(),
			commits_url: z.string(),
			git_commits_url: z.string(),
			comments_url: z.string(),
			issue_comment_url: z.string(),
			contents_url: z.string(),
			compare_url: z.string(),
			merges_url: z.string().url(),
			archive_url: z.string(),
			downloads_url: z.string().url(),
			issues_url: z.string(),
			pulls_url: z.string(),
			milestones_url: z.string(),
			notifications_url: z.string(),
			labels_url: z.string(),
			releases_url: z.string(),
			deployments_url: z.string().url(),
			git_url: z.string(),
			ssh_url: z.string(),
			clone_url: z.string(),
			svn_url: z.string().url(),
			forks: z.number().int(),
			open_issues: z.number().int(),
			watchers: z.number().int(),
			topics: z.array(z.string()).optional(),
			mirror_url: z.union([z.string().url(), z.null()]),
			has_issues: z.boolean(),
			has_projects: z.boolean(),
			has_pages: z.boolean(),
			has_wiki: z.boolean(),
			has_downloads: z.boolean(),
			has_discussions: z.boolean().optional(),
			archived: z.boolean(),
			disabled: z
				.boolean()
				.describe("Returns whether or not this repository disabled."),
			visibility: z
				.string()
				.describe("The repository visibility: public, private, or internal.")
				.optional(),
			license: z.union([
				z.null(),
				z
					.object({
						key: z.string(),
						name: z.string(),
						url: z.union([z.string().url(), z.null()]),
						spdx_id: z.union([z.string(), z.null()]),
						node_id: z.string(),
						html_url: z.string().url().optional(),
					})
					.describe("License Simple"),
			]),
			permissions: z
				.object({
					admin: z.boolean(),
					maintain: z.boolean().optional(),
					push: z.boolean(),
					triage: z.boolean().optional(),
					pull: z.boolean(),
				})
				.optional(),
			text_matches: z
				.array(
					z.object({
						object_url: z.string().optional(),
						object_type: z.union([z.string(), z.null()]).optional(),
						property: z.string().optional(),
						fragment: z.string().optional(),
						matches: z
							.array(
								z.object({
									text: z.string().optional(),
									indices: z.array(z.number().int()).optional(),
								}),
							)
							.optional(),
					}),
				)
				.optional(),
			temp_clone_token: z.string().optional(),
			allow_merge_commit: z.boolean().optional(),
			allow_squash_merge: z.boolean().optional(),
			allow_rebase_merge: z.boolean().optional(),
			allow_auto_merge: z.boolean().optional(),
			delete_branch_on_merge: z.boolean().optional(),
			allow_forking: z.boolean().optional(),
			is_template: z.boolean().optional(),
			web_commit_signoff_required: z.boolean().optional(),
		})
		.describe("Repo Search Result Item"),
);

export type RepoSearchResult = z.infer<typeof RepoSearchResult>;
