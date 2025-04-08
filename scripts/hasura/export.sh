# 1. Export the latest metadata from your running Hasura instance
hasura metadata export

# 2. Create migrations for any database changes (if needed)
hasura migrate create "your_change_description" --from-server