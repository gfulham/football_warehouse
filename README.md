Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test

### Ingest scripts

Install the Python dependencies in the environment used to run the ingest scripts:

```powershell
python -m pip install -r requirements.txt
```

The Snowflake pandas integration requires both pandas and PyArrow. Installing
`snowflake-connector-python[pandas]` from the requirements file supplies that
optional dependency.


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
