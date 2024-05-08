import json
import streamlit as st
import pandas as pd
import requests
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid 

_connection=None

def connect_to_mysql():
    global _connection
    if not _connection:
        _connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
        )

connect_to_mysql()

query1 = "SELECT * FROM phonpe_project.top_user"
cursor = _connection.cursor(buffered=True)
cursor.execute(query1)    
t1 = cursor.fetchall()
top_user = pd.DataFrame(t1, columns=["Type","State","year","Quarter","pincode","Registered_user"])

query2 = "SELECT * FROM phonpe_project.top_transaction"
cursor = _connection.cursor(buffered=True)
cursor.execute(query2)    
t2 = cursor.fetchall()
Top_Transaction = pd.DataFrame(t2, columns=["Type","State","location_pincode","year","Quarter","Transaction_count","Transaction_amount"])

query3 = "SELECT * FROM phonpe_project.map_user"
cursor = _connection.cursor(buffered=True)
cursor.execute(query3)    
t3 = cursor.fetchall()

map_user = pd.DataFrame(t3, columns=["Type","State","year","Quarter","District_Name","Registered_user","App_Open_count"])

query4 = "SELECT * FROM phonpe_project.map_transaction"
cursor = _connection.cursor(buffered=True)
cursor.execute(query4)    
t4 = cursor.fetchall()
map_transaction = pd.DataFrame(t4, columns=["Type","State","District_Name","year","Quarter","Transaction_count","Transaction_amount"])

query5 = "SELECT * FROM phonpe_project.aggregated_transaction"
cursor = _connection.cursor(buffered=True)
cursor.execute(query5)    
t5 = cursor.fetchall()
aggregated_transaction = pd.DataFrame(t5, columns=["Type","State","Payment_type","year","Quarter","Transaction_count","Transaction_amount"])

query6 = "SELECT * FROM phonpe_project.aggregated_user"
cursor = _connection.cursor(buffered=True)
cursor.execute(query6)    
t6 = cursor.fetchall()
aggregated_user = pd.DataFrame(t6, columns=["Type","State","year","Quarter","Registered_user","Mobile_brand","User_Count","User_Percentage"])



def Aggre_trans_Y(df,year):
    
    aiy= df[df["year"] == year]
    aiy.reset_index(drop= True, inplace= True)

    aiyg=aiy.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    aiyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(aiyg, x="State", y= "Transaction_amount",title= f"{year} TRANSACTION AMOUNT",
                           width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)
    with col2:

        fig_count= px.bar(aiyg, x="State", y= "Transaction_count",title= f"{year} TRANSACTION COUNT",
                          width=600, height= 650, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        State_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        State_name_tra.sort()
        

        fig_india_1= px.choropleth(aiyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Transaction_amount"].min(),aiyg["Transaction_amount"].max()),
                                 hover_name= "State",title = f"{year} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(aiyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Transaction_count"].min(),aiyg["Transaction_count"].max()),
                                 hover_name= "State",title = f"{year} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)

    return aiy


def Aggre_trans_Y_Q(df,quarter):
    aiyq= df[df["Quarter"] == quarter]
    aiyq.reset_index(drop= True, inplace= True)

    aiyqg= aiyq.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    aiyqg.reset_index(inplace= True)

    col1,col2= st.columns(2)

    with col1:
        fig_q_amount= px.bar(aiyqg, x= "State", y= "Transaction_amount", 
                            title= f"{aiyq['year'].min()} AND {quarter} TRANSACTION AMOUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(fig_q_amount)

    with col2:
        fig_q_count= px.bar(aiyqg, x= "State", y= "Transaction_count", 
                            title= f"{aiyq['year'].min()} AND {quarter} TRANSACTION COUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_q_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        State_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        State_name_tra.sort()

        fig_india_1= px.choropleth(aiyqg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Transaction_amount"].min(),aiyqg["Transaction_amount"].max()),
                                 hover_name= "State",title = f"{aiyq['year'].min()} AND {quarter} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)
    with col2:

        fig_india_2= px.choropleth(aiyqg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Transaction_count"].min(),aiyqg["Transaction_count"].max()),
                                 hover_name= "State",title = f"{aiyq['year'].min()} AND {quarter} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)
    
    return aiyq

        
def Aggre_user_plot_1(df,year):
    aguy= df[df["year"] == year]
    aguy.reset_index(drop= True, inplace= True)
    
    aguyg= pd.DataFrame(aguy.groupby("Mobile_brand")["User_Count"].sum())
    aguyg.reset_index(inplace= True)

    fig_line_1= px.bar(aguyg, x="Mobile_brand",y= "User_Count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_line_1)

    return aguy

def Aggre_user_plot_2(df,quarter):
    auqs= df[df["Quarter"] == quarter]
    auqs.reset_index(drop= True, inplace= True)

    fig_pie_1= px.pie(data_frame=auqs, names= "Mobile_brand", values="User_Count", hover_data= "User_Percentage",
                      width=1000,title=f"{quarter} QUARTER TRANSACTION COUNT PERCENTAGE",hole=0.5, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return auqs

def Aggre_user_plot_3(df,state):
    aguqy= df[df["State"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Mobile_brand")["User_Count"].sum())
    aguqyg.reset_index(inplace= True)

    fig_scatter_1= px.line(aguqyg, x= "Mobile_brand", y= "User_Count", markers= True,width=1000)
    st.plotly_chart(fig_scatter_1)

def Agg_map_trans_plot_1(df,state):
    miys= df[df["State"] == state]
    miysg= miys.groupby("District_Name")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "District_Name", y= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "District_Name", y= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              color_discrete_sequence= px.colors.sequential.Mint)
        
        st.plotly_chart(fig_map_bar_1)

def Agg_map_trans_plot_2(df,state):
    miys= df[df["State"] == state]
    miysg= miys.groupby("District_Name")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_pie_1= px.pie(miysg, names= "District_Name", values= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)

    with col2:
        fig_map_pie_1= px.pie(miysg, names= "District_Name", values= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_pie_1)

def map_user_plot_1(df, year):
    muy= df[df["year"] == year]
    muy.reset_index(drop= True, inplace= True)
    muyg= muy.groupby("State")[["Registered_user","App_Open_count"]].sum()
    muyg.reset_index(inplace= True)
    fig_combined = go.Figure()

    fig_combined= px.line(muyg, x= "State", y= ["Registered_user","App_Open_count"], markers= True,
                                width=1000,height=800,title= f"{year} REGISTERED USER AND APPOPENS", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_combined)

    return muy

def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"] == quarter]
    muyq.reset_index(drop= True, inplace= True)
    muyqg= muyq.groupby("State")[["Registered_user","App_Open_count"]].sum()
    muyqg.reset_index(inplace= True)
    fig_combined = go.Figure()

    fig_combined= px.line(muyqg, x= "State", y= ["Registered_user","App_Open_count"], markers= True,
                                title= f"{df['year'].min()}, {quarter} QUARTER REGISTERED USER AND APPOPENS",
                                width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_combined)

    return muyq

def map_user_plot_3(df, state):
    muyqs = df[df["State"] == state]
    muyqs.reset_index(drop=True, inplace=True)
    muyqsg = muyqs.groupby("District_Name")[["Registered_user", "App_Open_count"]].sum()
    muyqsg.reset_index(inplace=True)

    fig_combined = go.Figure()

    fig_combined.add_trace(go.Bar(x=muyqsg["District_Name"], y=muyqsg["Registered_user"], name="Registered Users", marker_color='rgb(55, 83, 109)'))
    fig_combined.add_trace(go.Bar(x=muyqsg["District_Name"], y=muyqsg["App_Open_count"], name="App Opens", marker_color='rgb(26, 118, 255)'))

    fig_combined.update_layout(title=f'{state.upper()} Registered Users vs App Opens',
                               xaxis_title='District',
                               yaxis_title='Count',
                               barmode='group')

    st.plotly_chart(fig_combined)

def top_user_plot_1(df,year):
    tuy= df[df["year"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["State","Quarter"])["Registered_user"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "State", y= "Registered_user", barmode= "group", color= "Quarter",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plot_1)

    return tuy

def top_user_plot_2(df,state):
    tuys= df[df["State"] == state]
    tuys.reset_index(drop= True, inplace= True)

    tuysg= pd.DataFrame(tuys.groupby("Quarter")["Registered_user"].sum())
    tuysg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuys, x= "Quarter", y= "Registered_user",barmode= "group",
                           width=1000, height= 800,color= "Registered_user",hover_data="pincode",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_1)

#Streamlit part

st.set_page_config(layout= "wide")

st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
st.write("")

with st.sidebar:
    
    select= option_menu("Main Menu",["Home", "Explore Data", "Insights"])


if select == "Home":
    st.image("C:/Users/BARATH KANNAN/OneDrive/Desktop/Phone_pe.jpg", caption="WELCOME TO DATA INSIGHT", use_column_width=True)
 
    

     

if select == "Explore Data":
    tab1, tab2, tab3= st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method = st.radio("**Select the Analysis Method**",["Transaction Analysis", "User Analysis"])

            
        if method == "Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                year_at= st.slider("**Select the Year**", aggregated_transaction["year"].min(), aggregated_transaction["year"].max(),aggregated_transaction["year"].min())

            df_agg_tran_Y= Aggre_trans_Y(aggregated_transaction,year_at)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_at= st.slider("**Select the Quarter**", df_agg_tran_Y["Quarter"].min(), df_agg_tran_Y["Quarter"].max(),df_agg_tran_Y["Quarter"].min())

            df_agg_tran_Y_Q= Aggre_trans_Y_Q(df_agg_tran_Y, quarters_at)


        elif method == "User Analysis":
            year_au= st.selectbox("Select the Year_AU",aggregated_user["year"].unique())
            agg_user_Y= Aggre_user_plot_1(aggregated_user,year_au)

            quarter_au= st.selectbox("Select the Quarter_AU",agg_user_Y["Quarter"].unique())
            agg_user_Y_Q= Aggre_user_plot_2(agg_user_Y,quarter_au)

            state_au= st.selectbox("**Select the State_AU**",agg_user_Y["State"].unique())
            Aggre_user_plot_3(agg_user_Y_Q,state_au)

    with tab2:
        method_map = st.radio("**Select the Analysis Method(MAP)**",["Map Transaction Analysis", "Map User Analysis"])

        if method_map == "Map Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                year_m2= st.slider("**Select the Year_mi**", map_transaction["year"].min(), map_transaction["year"].max(),map_transaction["year"].min())

            df_map_tran_Y= Aggre_trans_Y(map_transaction, year_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m3= st.selectbox("Select the State_mi", df_map_tran_Y["State"].unique())

            Agg_map_trans_plot_1(df_map_tran_Y,state_m3)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m2= st.slider("**Select the Quarter_mi**", df_map_tran_Y["Quarter"].min(), df_map_tran_Y["Quarter"].max(),df_map_tran_Y["Quarter"].min())

            df_map_tran_Y_Q= Aggre_trans_Y_Q(df_map_tran_Y, quarters_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m4= st.selectbox("Select the State_miy", df_map_tran_Y_Q["State"].unique())            
            
            Agg_map_trans_plot_2(df_map_tran_Y_Q, state_m4)

        elif method_map == "Map User Analysis":
            col1,col2= st.columns(2)
            with col1:
                year_mu1= st.selectbox("**Select the Year_mu**",map_user["year"].unique())
            map_user_Y= map_user_plot_1(map_user, year_mu1)

            col1,col2= st.columns(2)
            with col1:
                quarter_mu1= st.selectbox("**Select the Quarter_mu**",map_user_Y["Quarter"].unique())
            map_user_Y_Q= map_user_plot_2(map_user_Y,quarter_mu1)

            col1,col2= st.columns(2)
            with col1:
                state_mu1= st.selectbox("**Select the State_mu**",map_user_Y_Q["State"].unique())
            map_user_plot_3(map_user_Y_Q, state_mu1)

    with tab3:
        method_top = st.radio("**Select the Analysis Method(TOP)**",["Top Transaction Analysis", "Top User Analysis"])
       
        if method_top == "Top Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                year_t2= st.slider("**Select the Year_tt**", Top_Transaction["year"].min(), Top_Transaction["year"].max(),Top_Transaction["year"].min())
 
            df_top_tran_Y= Aggre_trans_Y(Top_Transaction,year_t2)

            
            col1,col2= st.columns(2)
            with col1:
                quarters_t2= st.slider("**Select the Quarter_tt**", df_top_tran_Y["Quarter"].min(), df_top_tran_Y["Quarter"].max(),df_top_tran_Y["Quarter"].min())

            df_top_tran_Y_Q= Aggre_trans_Y_Q(df_top_tran_Y, quarters_t2)

        elif method_top == "Top User Analysis":
            col1,col2= st.columns(2)
            with col1:
                year_t3= st.selectbox("**Select the Year_tu**", top_user["year"].unique())

            df_top_user_Y= top_user_plot_1(top_user,year_t3)

            col1,col2= st.columns(2)
            with col1:
                state_t3= st.selectbox("**Select the State_tu**", df_top_user_Y["State"].unique())

            df_top_user_Y_S= top_user_plot_2(df_top_user_Y,state_t3)


if select == "Insights":
    question=st.sidebar.selectbox("Select Question",("Select your question",
                                    "Top 10 States by highest Transaction Amount",
                                    "Top 10 States by Lowest Transaction Amount",
                                    "Top 10 Districts by Highest Transaction Amount",
                                    "Top 10 Districts by Lowest Transaction Amount",
                                    "Top 10 States lowest With AppOpens",
                                    "Top 10 Highest States With AppOpens",
                                    "States with Lowest Transaction Count",
                                    "States with Highest Transaction Count",
                                    "Top Mobile Brands by User Count",
                                    "State with Lowest Transaction Amount in 2021"))

    if question== "Select your question":
         st.image("C:/Users/BARATH KANNAN/OneDrive/Desktop/Phone_pe_home.png", caption="WELCOME TO DATA INSIGHT", use_column_width=True)
      
      
       
    elif question== "Top 10 States by highest Transaction Amount":
        col1,col2=st.columns(2)
        with col1:
         data = aggregated_transaction[["State", "Transaction_amount"]]
         data1 = data.groupby("State")["Transaction_amount"].sum().sort_values(ascending=False)
         data2 = pd.DataFrame(data1).reset_index().head(10)

         fig_data = px.bar(data2, x="State", y="Transaction_amount", 
                        title="Top 10 States by highest Transaction Amount", 
                        color="State",
                        color_discrete_sequence=px.colors.sequential.Oranges_r)
         st.plotly_chart(fig_data)
        with col2:
            query1='''SELECT State, SUM(Transaction_amount) AS TRANSACTION_AMOUNT FROM phonpe_project.aggregated_transaction
            group by State 
            order by TRANSACTION_AMOUNT desc
            LIMIT 10;'''
            mycursor=_connection.cursor(buffered=True)
            mycursor.execute(query1)
            t1=mycursor.fetchall()
            df1=pd.DataFrame(t1,columns=["State","TRANSACTION_AMOUNT"])
            AgGrid(df1)  

    elif question== "Top 10 States by Lowest Transaction Amount":
        col1,col2=st.columns(2)
        with col1:
         data = aggregated_transaction[["State", "Transaction_amount"]]
         data1 = data.groupby("State")["Transaction_amount"].sum().sort_values(ascending=True)
         data2 = pd.DataFrame(data1).reset_index().head(10)

         fig_data = px.bar(data2, x="State", y="Transaction_amount", 
                        title="Top 10 States by Lowest Transaction Amount", 
                        color="State",
                        color_discrete_sequence=px.colors.sequential.Oranges_r)
         st.plotly_chart(fig_data)
        with col2:
            query2='''SELECT State, SUM(Transaction_amount) AS TRANSACTION_AMOUNT FROM phonpe_project.aggregated_transaction
            group by State 
            order by TRANSACTION_AMOUNT 
            LIMIT 10;'''
            mycursor=_connection.cursor(buffered=True)
            mycursor.execute(query2)
            t2=mycursor.fetchall()
            df2=pd.DataFrame(t2,columns=["State","TRANSACTION_AMOUNT"])
            AgGrid(df2)


    elif question== "Top 10 Districts by Highest Transaction Amount":
         data = map_transaction[["District_Name", "Transaction_amount"]]
         data1 = data.groupby("District_Name")["Transaction_amount"].sum().sort_values(ascending=False)
         data2 = pd.DataFrame(data1).head(10).reset_index()
         fig_data = px.bar(data2, x="District_Name", y="Transaction_amount", 
                        title="Top 10 Districts by Highest Transaction Amount", 
                        color="District_Name",
                        color_discrete_sequence=px.colors.sequential.Emrld_r)
         st.plotly_chart(fig_data)

         query3='''SELECT District, SUM(Transaction_amount) AS TRANSACTION_AMOUNT FROM phonpe_project.map_transaction
            group by District 
            order by TRANSACTION_AMOUNT desc
            LIMIT 10;'''
         mycursor=_connection.cursor(buffered=True)
         mycursor.execute(query3)
         t3=mycursor.fetchall()
         df3=pd.DataFrame(t3,columns=["District","TRANSACTION_AMOUNT"])
         AgGrid(df3)    

      
    elif question== "Top 10 Districts by Lowest Transaction Amount":
        data = map_transaction[["District_Name", "Transaction_amount"]]
        data1 = data.groupby("District_Name")["Transaction_amount"].sum().sort_values(ascending=True)
        data2 = pd.DataFrame(data1).head(10).reset_index()
        fig_data = px.bar(data2, x="District_Name", y="Transaction_amount", 
                        title="Top 10 Districts by Lowest Transaction Amount", 
                        color="District_Name",
                        color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig_data)

        query4='''SELECT District, SUM(Transaction_amount) AS TRANSACTION_AMOUNT FROM phonpe_project.map_transaction
            group by District 
            order by TRANSACTION_AMOUNT 
            LIMIT 10;'''
        mycursor=_connection.cursor(buffered=True)
        mycursor.execute(query4)
        t4=mycursor.fetchall()
        df4=pd.DataFrame(t4,columns=["District","TRANSACTION_AMOUNT"])
        AgGrid(df4) 

    elif question== "Top 10 States lowest With AppOpens":
        data= map_user[["State", "App_Open_count"]]
        data1= data.groupby("State")["App_Open_count"].sum().sort_values(ascending=True)
        data2= pd.DataFrame(data1).reset_index().head(10)

        fig_data= px.bar(data2, x= "State", y= "App_Open_count", title="Top 10 States lowest With AppOpens",
                  color_discrete_sequence= px.colors.sequential.Blues_r)
        st.plotly_chart(fig_data)

        query5='''SELECT State, SUM(App_Open_count) AS APP_OPENS FROM phonpe_project.map_user
            group by State 
            order by APP_OPENS 
            LIMIT 10;'''
        mycursor=_connection.cursor(buffered=True)
        mycursor.execute(query5)
        t5=mycursor.fetchall()
        df5=pd.DataFrame(t5,columns=["District","APP_OPENS"])
        AgGrid(df5) 


    elif question== "Top 10 Highest States With AppOpens":
      data= map_user[["State", "App_Open_count"]]
      data1= data.groupby("State")["App_Open_count"].sum().sort_values(ascending=False)
      data2= pd.DataFrame(data1).reset_index().head(10)

      fig_sa= px.bar(data2, x= "State", y= "App_Open_count", title="Top 10 Lowest States With AppOpens",
                  color_discrete_sequence= px.colors.sequential.Blues_r)
      st.plotly_chart(fig_sa)

      query6='''SELECT State, SUM(App_Open_count) AS APP_OPENS FROM phonpe_project.map_user
            group by State 
            order by APP_OPENS DESC
            LIMIT 10;'''
      mycursor=_connection.cursor(buffered=True)
      mycursor.execute(query6)
      t6=mycursor.fetchall()
      df6=pd.DataFrame(t6,columns=["District","APP_OPENS"])
      AgGrid(df6) 

    elif question== "States with Lowest Transaction Count":

      data = aggregated_transaction[["State", "Transaction_count"]]
      data1 = data.groupby("State")["Transaction_count"].sum().sort_values(ascending=True)
      data2 = pd.DataFrame(data1).reset_index().head(10)

      fig_data = px.bar(data2, x="State", y="Transaction_count", 
                     title="States with Lowest Transaction Count", 
                     color="State",
                     color_discrete_sequence=px.colors.sequential.Jet_r)

      st.plotly_chart(fig_data)

      query7='''SELECT State, SUM(Transaction_Count) AS TRANSACTION_COUNT FROM phonpe_project.aggregated_transaction
            group by State 
            order by TRANSACTION_COUNT 
            LIMIT 10;'''
      mycursor=_connection.cursor(buffered=True)
      mycursor.execute(query7)
      t7=mycursor.fetchall()
      df7=pd.DataFrame(t7,columns=["State","TRANSACTION_COUNT"])
      AgGrid(df7)  


    elif question== "States with Highest Transaction Count":

      data = aggregated_transaction[["State", "Transaction_count"]]
      data1 = data.groupby("State")["Transaction_count"].sum().sort_values(ascending=False)
      data2 = pd.DataFrame(data1).reset_index().head(10)

      fig_data = px.bar(data2, x="State", y="Transaction_count", 
                     title="States with Highest Transaction Count", 
                     color="State",
                     color_discrete_sequence=px.colors.sequential.Jet_r)

      st.plotly_chart(fig_data)

      query8='''SELECT State, SUM(Transaction_Count) AS TRANSACTION_COUNT FROM phonpe_project.aggregated_transaction
            group by State 
            order by TRANSACTION_COUNT DESC
            LIMIT 10;'''
      mycursor=_connection.cursor(buffered=True)
      mycursor.execute(query8)
      t8=mycursor.fetchall()
      df8=pd.DataFrame(t8,columns=["State","TRANSACTION_COUNT"])
      AgGrid(df8)  

    elif question== "Top Mobile Brands by User Count":
        col1,col2=st.columns(2)
        with col1:
         data = aggregated_user[["Mobile_brand", "User_Count"]]
         data1 = data.groupby("Mobile_brand")["User_Count"].sum().sort_values(ascending=False)
         data2 = pd.DataFrame(data1).reset_index()

         fig_data = px.bar(data2, x="Mobile_brand", y="User_Count", 
                           title="Top Mobile Brands by User Count", 
                           color="Mobile_brand",
                           color_discrete_sequence=px.colors.sequential.dense_r)

         st.plotly_chart(fig_data)
        with col2:
               query9='''SELECT Mobile_brand, SUM(User_Count) AS USER_COUNT FROM phonpe_project.aggregated_user
        group by Mobile_brand 
        order by USER_COUNT desc;'''
        mycursor=_connection.cursor(buffered=True)
        mycursor.execute(query9)
        t9=mycursor.fetchall()
        df9=pd.DataFrame(t9,columns=["Mobile_brand","User_Count"])
        AgGrid(df9)       

    elif question== "State with Lowest Transaction Amount in 2021":
      data = Top_Transaction[Top_Transaction['year'] == 2021][["State", "Transaction_amount"]]
      data1 = data.groupby("State")["Transaction_amount"].sum().sort_values(ascending=True)
      data2 = pd.DataFrame(data1).reset_index().head(10)

      fig_data = px.bar(data2, x="State", y="Transaction_amount", 
                     title="State with Lowest Transaction Amount in 2021", 
                     color="State",
                     color_discrete_sequence=px.colors.sequential.Mint_r)
      st.plotly_chart(fig_data)

      query1='''SELECT State, SUM(Transaction_amount) AS TRANSACTION_AMOUNT FROM phonpe_project.Top_Transaction
      where year=2021
      group by State
      order by TRANSACTION_AMOUNT ;'''
      mycursor=_connection.cursor(buffered=True)
      mycursor.execute(query1)
      t10=mycursor.fetchall()
      df10=pd.DataFrame(t10,columns=["State","TRANSACTION_AMOUNT"])
      AgGrid(df10) 
