from utils import create_server_context
from query import select_rows, execute_sql

print("Create a server context")
server_context = create_server_context('10.10.10.178:8080', 'CDSTest Project', 'labkey', use_ssl=False)

# ssr = select_rows('study', 'Demographics', server_context)
# if ssr is not None:
#     print("select_rows: There are " + str(ssr['rowCount']) + " rows.")
# else:
#     print('select_rows: Failed to load results from study.Demographics')
#
# # ssr = select_rows('study', 'Demographics', server_context, max_rows=17)
# # if ssr is not None:
# #     print("There are " + str(len(ssr['rows'])) + " rows.")
# # else:
# #     print('Failed to load 17 rows from study.Demographics')
#
# ssr = select_rows('study', 'Demographics404', server_context)
#
# esr = execute_sql('study', 'SELECT * FROM Demographics', server_context)
# print("execute_sql: There are " + str(len(esr['rows'])) + " rows.")

ssr = select_rows('study', 'Demographics', server_context, max_rows=5)
print("select_rows: There are " + str(len(ssr['rows'])) + " rows.")