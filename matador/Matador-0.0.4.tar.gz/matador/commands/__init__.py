from .hello import Hello
from .run_sql_script import RunSqlScript
from .deploy_ticket import DeployTicket

commands = {
    'hello': Hello,
    'run-sql-script': RunSqlScript,
    'deploy-ticket': DeployTicket
}
