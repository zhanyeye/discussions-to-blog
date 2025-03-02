# discussions-to-blog  

A GitHub Action to sync GitHub Discussions from a specific category to Markdown files, making it easy to use them in static site generators like Hugo or Jekyll.  

## Inputs  

| Name              | Description                                      | Required | Default         |  
|-------------------|--------------------------------------------------|----------|-----------------|  
| `github_token`    | GitHub token for accessing the GraphQL API.      | Yes      | N/A             |  
| `repo_owner`      | The owner of the repository.                     | Yes      | N/A             |  
| `repo_name`       | The name of the repository.                      | Yes      | N/A             |  
| `category_id`     | The ID of the Discussions category.              | Yes      | N/A             |  
| `output_dir`      | The directory to save Markdown files.            | No       | `content/posts` |  
| `delete_on_removed` | Whether to delete Markdown files for removed Discussions. | No       | `false`         |  

## Example Usage  

```yaml  
name: Sync Discussions to Blog  

on:  
  schedule:  
    - cron: "0 * * * *"  

jobs:  
  sync-discussions:  
    runs-on: ubuntu-latest  
    steps:  
      - name: Checkout repository  
        uses: actions/checkout@v3  

      - name: Sync Discussions  
        uses: zhanyeye/discussions-to-blog@v1
        with:  
          github_token: ${{ secrets.GITHUB_TOKEN }}  
          repo_owner: your-org  
          repo_name: your-repo  
          category_id: your-category-id  
          output_dir: content/posts  
          delete_on_removed: "true"
      
      - name: Commit and Push Changes  
        uses: stefanzweifel/git-auto-commit-action@v4  
        with:  
          commit_message: "Sync Discussions to Markdown"  
          branch: main  
          file_pattern: content/posts/**/*