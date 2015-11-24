from .run_sql_script import RunSqlScript
from .deploy_ticket import DeployTicket, RemoveTicket

commands = {
    'run-sql-script': RunSqlScript,
    'deploy-ticket': DeployTicket,
    'remove-ticket': RemoveTicket
}
