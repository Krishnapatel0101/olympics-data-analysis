import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://th.bing.com/th/id/R.587281d2843682394fe930a490667dbd?rik=un%2fm8Mwiidf8zg&riu=http%3a%2f%2fpluspng.com%2fimg-png%2folympic-rings-png-hd-olympic-rings-transparent-background-3-2000.png&ehk=bhICF%2fiq3ZoDBD2VZZUh92dPXPKuYiMEoW7c8bz0p6E%3d&risl=&pid=ImgRaw&r=0')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Rank list','Overall Analysis','Top athletes of country','Athlete wise Analysis','Country and Year wise details','Athlete details')
)

if user_menu == 'Rank list':
    st.sidebar.header("Rank list")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Rank list")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="count", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="count", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="count", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True,ax=ax)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Top athletes of country':

    st.title('Country')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.selectbox('Select a Country',country_list)

    st.title("Top athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)
if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig_age = plt.figure(figsize=(10, 6))
    plt.hist([x1, x2, x3, x4], bins=30, label=['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
             histtype='step', density=True, color=['blue', 'gold', 'silver', 'brown'])
    st.title("Distribution of Age")
    plt.xlabel("Age")
    plt.ylabel("Probability Density")
    plt.legend()
    st.pyplot(fig_age)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)

    fig_gender = px.line(final, x="Year", y=["Male", "Female"],
                         title="Men Vs Women Participation Over the Years")
    fig_gender.update_layout(width=800, height=500)
    st.plotly_chart(fig_gender)

    sport_list = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)

    fig, ax = plt.subplots()
    sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', s=60, ax=ax)
    st.pyplot(fig)

if user_menu == 'Country and Year wise details':
    countries = df['region'].unique()
    selected_country = st.selectbox('Select a Country', countries)

    years = df['Year'].unique()
    years.sort()
    selected_year = st.selectbox('Select a Year', years)

    filtered_df = df[(df['region'] == selected_country) & (df['Year'] == selected_year)]

    st.title(f"Player Details for {selected_country} in {selected_year}")

    medal_table = filtered_df[['Name', 'Age', 'Sex', 'Sport', 'Medal']]
    st.table(medal_table)

if user_menu == 'Athlete details':
    athlete_names = df['Name'].unique()
    selected_athlete = st.selectbox('Select an Athlete', athlete_names)

    athlete_details = df[df['Name'] == selected_athlete].iloc[0]

    st.title(f"Details for Athlete: {selected_athlete}")
    st.write("Name:", athlete_details['Name'])
    st.write("Age:", athlete_details['Age'])
    st.write("Sex:", athlete_details['Sex'])
    st.write("Sport:", athlete_details['Sport'])
    st.write("Nationality:", athlete_details['region'])

    st.title("Medals Won")
    medals_table = df[(df['Name'] == selected_athlete) & (df['Medal'].notna())][['Year', 'Sport', 'Medal']]
    st.table(medals_table)









