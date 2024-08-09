import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import plotly.express as px

#import dataset
df = pd.read_csv('https://raw.githubusercontent.com/rini3636/DSC205_FinalProject/main/batVbug_cleaned.csv')

#Introduce project
st.image('https://kubrick.htvapps.com/htv-prod-media.s3.amazonaws.com/images/pallid-bat-usfws-652c515332a61.png?crop=1.00xw:0.878xh;0,0.122xh&resize=900:*',
         caption='Antrozous pallidus bat saying hello - 143 Calls were identified from this species during this study')
st.title('Exploring the Diversity of Bats in the Grand Canyon')

st.image('https://media.istockphoto.com/id/484207740/vector/beats.jpg?s=612x612&w=0&k=20&c=p9EiZDOn9Lm3n8iOLv5KwpU3cqj0CIghI2Wgg9xQGb0=', width = 76)

##Start with some info
st.header('Introduction:')
st.markdown('What do you know about bats?')

#Engage with question, make viewer think about what they think they know
with st.form(key='my_form1'):
    choice1 = st.slider('How many species of bats do you think there are?',300, 1500, 100 )
    submitted = st.form_submit_button(label='Guess')
if submitted:
    if choice1 >= 1400:
        st.markdown("Great Job!")
        st.markdown('Correct answer: Over 1,400')
    else:
        st.markdown('Correct answer: Over 1,400')
    st.markdown("Bats are the second most diverse group of mammals. Only rodents have more types of species. Compared to other groups such as primates that only have about unique living 500 species, bats are pretty special.")
    st.markdown("Let's take a look at an example of this diversity through a study that recorded bat activity at the Grand Canyon in Arizona.")

#Lead to study & goals
st.subheader("The Study")
st.markdown("From 2017-2020, volunteers conducted a study in a ____km region of the grand canyon, using acoustic recorders to identify bats in the area.")
st.markdown("We'll use this study to learn about the bats of the area, and give an insight on bat diversity in general.")
st.subheader("We will see:")
st.markdown("""
- What the species diversity in this area looks like
- Where these species were identified
- What allows them to coexist
""")

st.image('https://media.istockphoto.com/id/484207740/vector/beats.jpg?s=612x612&w=0&k=20&c=p9EiZDOn9Lm3n8iOLv5KwpU3cqj0CIghI2Wgg9xQGb0=', width = 76)

##New section: What species
st.header('What does the diversity in this area looks like?')
st.subheader('Treemap Representing Total Composition of Bats Identified')
#Taxon count data (easier format for putting treemap together)
bat_types = pd.read_csv('https://raw.githubusercontent.com/rini3636/DSC205_FinalProject/main/bat_taxon3.csv')

#Setting up treemap
genus = bat_types['Genus']
species = bat_types['Species']
count = bat_types['Count']
#Wanted to add some extra info in the boxes but couldn't get it working
percent = bat_types['Percent']
#Was going to put a picture of PAHE because it was the most common and I wanted to draw attention to it
image = bat_types['Image']

fig = px.treemap(bat_types, 
path=[genus, species],
values=count,
title='22 Species Belonging to 9 Genera'
)
#Little details of treemap
fig.update_layout(
    #I really tried to match this font to everything else, but it didn't work
    title_font_family='Arial',
    title_font_size= 25,
)
#Printing treemap
st.plotly_chart(fig, use_container_width=False)

#Explain treemap
st.markdown('''-The treemap above represents all of the bats that were successfully identified down to the species during this study.''')
st.markdown('''-The larger rectangles represent a unique genus. You can click on each genus to view the species belonging to it that were identified during the study.\n''')
st.markdown('''-The size of the rectangle shows the number of times that type of bat was identified.''')

st.image('https://media.istockphoto.com/id/484207740/vector/beats.jpg?s=612x612&w=0&k=20&c=p9EiZDOn9Lm3n8iOLv5KwpU3cqj0CIghI2Wgg9xQGb0=', width = 76)

##New Section: Go over location data
st.header('Where were the bats?')
st.subheader('Map of sites where activity was recorded')

# Choose year
year = st.radio('Select year', ('2017', '2018', '2019', '2020'))
month = st.slider('Select month', 4, 10)

# Filter based on selected year and month
if year == '2020' and month <= 5:
    st.markdown("No data was collected for this month")
else:
    monthyear = year + '-' + str(month)
    filtered_df1 = df.loc[df['YearMonth'] == monthyear]
    st.markdown(monthyear)

    # Showing map
    m = folium.Map(location=[36.305468300947624, -112.92260158674561], zoom_start=8)
    
    for index, row in filtered_df1.iterrows():
        loc = [row['Latitude'], row['Longitude']]
        #Filter species with counts > 0 and create the label
        species_counts = row[['ANPA', 'COTO', 'EPFU', 'EUMA', 'EUPE', 
                              'LABL', 'LACI', 'LANO', 'LAXA', 'MYCA', 
                              'MYCI', 'MYEV', 'MYGR', 'MYLU', 'MYTH', 
                              'MYVO', 'MYYU', 'NYFE', 'NYMA', 'PAHE', 
                              'PESU', 'TABR']]

        species_found = [f"{species}: {count}" for species, count in species_counts.items() if count > 0]
        loc_label = f"Species found at this site:\n" + "\n".join(species_found)
        c = folium.Marker(location=loc, popup=loc_label, tooltip='Site of recording')
        c.add_to(m)
    
    # Call to render Folium map in Streamlit
    st_data = st_folium(m, width=725)
st.markdown('''-By exploring the map, it's clear that different species of bat can be active around the same site at the same time.''')
st.markdown('''-When animals with similar diets and hunting methods live in the same area, it's expected that one should outcompete the other, leading to less diversity.
--Given this fact, would you expect the bats in this study have similar diets and hunting methods?
''')
with st.form(key='my_form2'):
    more_choice = st.radio('What do you think?', ('Similar', 'Not similar'))
    submitted = st.form_submit_button(label='Guess')
if submitted:
    if more_choice == 'Not similar':
        st.markdown('Good thinking, but...')
    else: 
        st.markdown('Correct')
    st.markdown('''Not similar would make sense, because it would lead to more diverse species remaining, like we see in the map,
        but they actually all eat similar insects''')
st.image('https://media.istockphoto.com/id/484207740/vector/beats.jpg?s=612x612&w=0&k=20&c=p9EiZDOn9Lm3n8iOLv5KwpU3cqj0CIghI2Wgg9xQGb0=', width = 76)

#New section: What allows them to coexist?
st.header('What allows them to coexist?')
st.subheader('Differing Hunting times allow for niche partitioning')
#Comparing time after sunset for PAHE and Myotis
#Filtering so it's just the times for PAHE and myotis
filtered_df2 = df.loc[:, ['MYCA','MYCI', 'MYEV', 'MYGR', 
                          'MYLU', 'MYTH', 'MYVO', 'MYYU',
                          'PAHE', 'MinStartPostSunset']]

filtered_df2['TotalMyotis'] = filtered_df2.loc[:, 'MYCA':'MYYU'].sum(axis=1)

#Filtering instances for Myotis and PAHE
instances_Myotis = filtered_df2.loc[filtered_df2['TotalMyotis'] > 0].copy()
instances_PAHE = filtered_df2.loc[filtered_df2['PAHE'] > 0].copy()

#Adding column labels
instances_Myotis['Species Group'] = 'Small Myotis Bats'
instances_PAHE['Species Group'] = 'PAHE'

#Prep x-ax
instances_Myotis['Number of Bats Recorded'] = instances_Myotis['TotalMyotis']
instances_PAHE['Number of Bats Recorded'] = instances_PAHE['PAHE']

#glue together dataframes
combined_df = pd.concat([instances_Myotis, instances_PAHE])

#Plotting scatterplot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=combined_df, 
                x='MinStartPostSunset', 
                y='Number of Bats Recorded', 
                hue='Species Group',
                style='Species Group',
                s=100)

plt.title('Bat Activity Relative to Minutes Past Sunset')
plt.xlabel('Minutes Past Sunset')
plt.ylabel('Number of Bats Recorded')
plt.legend(title='Species Group')

st.pyplot(plt)
st.markdown("At least that's what it said in the article that was written to accompany this dataset, but I couldn't get it to work.")


