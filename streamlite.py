# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title("Projet module architecture BI")

st.write(
    """Laura VERCHERE & Liam HUISSOUD
    """
)
st.write(
    """Classe : 2D
    """
)
st.write(
    """
    """
)

# Get the current credentials
session = get_active_session()


st.subheader("TOP 10 DES JOBS")
st.write(
    """Quel est le top 10 de job titles les plus postés ?
    """
)
 
# execute sql statement
sql = f"SELECT title, COUNT(*) AS job_count FROM jobs_posting GROUP BY title ORDER BY job_count DESC LIMIT 10 "
data = session.sql(sql).collect()

# Create a simple bar chart
st.bar_chart(data=data, x="TITLE", y="JOB_COUNT")
st.table(data)


#st.subheader("Underlying data")
#st.dataframe(data, use_container_width=True)

st.write(
    """
    """
)

st.subheader("JOB LE MIEUX RÉMUNÉRÉ")
st.write(
    """Quel est le job le mieux rémunéré (tenir compte de la devise) ?
    Ici, la devise est en USD.
    """
)
# execute sql statement
sql = f"SELECT jp.title, MAX(COALESCE(s.max_salary, 0)) AS max_salary FROM jobs_posting jp JOIN salaries_view s ON jp.job_id = s.job_id WHERE s.currency = 'USD' GROUP BY jp.title ORDER BY max_salary DESC LIMIT 1;"
data = session.sql(sql).collect()

# Create a simple bar chart
st.table(data)

st.write(
    """
    """
)

st.subheader("OFFRE D'EMPLOI PAR TAILLE D'ENTREPRISE")
st.write(
    """Quelle est la répartition des offres d’emploi par taille d’entreprise ?
    """
)
# execute sql statement
sql = f"SELECT c.company_size, COUNT(*) AS job_count FROM jobs_posting jp JOIN companies c ON jp.company_id = c.company_id GROUP BY c.company_size ORDER BY job_count DESC;"
data = session.sql(sql).collect()


# Create a simple bar chart
st.bar_chart(data=data, x="COMPANY_SIZE", y="JOB_COUNT")
st.table(data)

st.write(
    """
    """
)

st.subheader("OFFRE D'EMPLOI PAR TYPE D'INDUSTRIE")
st.write(
    """Quelle est la répartition des offres d’emploi par type d’industrie ?
    """
)

# Use an interactive slider to get user input
num_industry = st.slider(
    "Nombre d'industrie",
    min_value=1,
    max_value=212,
    value=106
)

# execute sql statement
sql = f"SELECT i.industry_name, COUNT(*) AS job_count FROM jobs_posting jp JOIN job_industries_view ji ON jp.job_id = ji.job_id JOIN industries_view i ON ji.industry_id = i.industry_id GROUP BY i.industry_name ORDER BY job_count DESC LIMIT " + str(num_industry)
data = session.sql(sql).collect()

# Create a simple bar chart
st.bar_chart(data=data, x="INDUSTRY_NAME", y="JOB_COUNT")
#st.table(data)

st.write(
    """
    """
)

st.subheader("OFFRE D'EMPLOI PAR TYPE D'EMPLOI")
st.write(
    """Quelle est la répartition des offres d’emploi par type d’emploi (full-time, intership, part-time) ?
    """
)

# execute sql statement
sql = f"SELECT jp.formatted_work_type, COUNT(*) AS job_count FROM jobs_posting jp GROUP BY jp.formatted_work_type ORDER BY job_count DESC"
data = session.sql(sql).collect()

# Create a simple bar chart
st.bar_chart(data=data, x="FORMATTED_WORK_TYPE", y="JOB_COUNT")
