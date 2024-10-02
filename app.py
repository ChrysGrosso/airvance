import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def main():
    st.title("Construction and HVAC markets")
    
    # Menu sur le côté avec le composant sidebar
    st.sidebar.title("Airvance-MI-Database")
    choix = st.sidebar.selectbox("Choose a tab", ["Construction market", "HVAC market"])

    if choix == "Construction market":
        data = pd.read_excel("euroconstruct_totaux_%_constant.xlsx")
        data2 = pd.read_excel("euroconstruct_detailed_NR_totaux.xlsx")
        #to skip a line : st.markdown('<script>window.scrollTo(0,0);</script>', unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### Page 1 - Euroconstruct forecasts on Construction market", unsafe_allow_html=True)
        st.markdown("_2024 Euroconstruct Summer edition - ref year : 2023_")
        #st.markdown("### Airvance Group's trading area")
        st.write("""
            <style>
                p {
                    text-align: justify;
                }
            </style>
            <p>Explore the customized Euroconstruct results for Airvance Group's catchment area, curated by Corporate Market Intelligence. \
                 You will find interactive charts and downloadable summary files,\
                 highlighting key market volume indicators and trends to support your data-driven decision-making.</p>
             """, unsafe_allow_html=True)
        
        
        
        st.write("""
            <style>
                p {
                    text-align: justify;
                }
            </style>
            <p>We invite you to discover the results for the country and years you are interested in.</p>
             """, unsafe_allow_html=True)
       
        # Sélection des filtres
        selected_countries = st.multiselect('Select the country. For an overview of the Airvance groups\'s catchment area, select \'All Countries\'', options=data['Country'].unique())
        st.subheader("Construction market trends (level at constant price)")
        st.write("_Ref year : 2023. 'R&M' stands for Renovation (Repairs and Maintenance), 'New' for Construction_")
       

        # Filtrer les données en fonction des filtres sélectionnés
        if selected_countries:
            filtered_data = data[data['Country'].isin(selected_countries)].copy()
            filtered_data2 = data2[data2['Country'].isin(selected_countries)].copy()
        else:
            filtered_data = data.copy()
            filtered_data2 = data2.copy()

        # Formater les colonnes du premier Dataframe
        if 'Market (constant €)' in filtered_data.columns:
            filtered_data['Year'] = filtered_data['Year'].astype(str)
            filtered_data['Market (constant Billion €)'] = filtered_data['Market (constant €)'] / 1e9
        else:
            st.error("The requested columns are not available in the filtered data.")
        
        # Formater les colonnes du deuxième Dataframe
        if 'Market (constant €)' in filtered_data2.columns:
            filtered_data2['Year'] = filtered_data2['Year'].astype(str)
            filtered_data2['Market (constant Billion €)'] = filtered_data2['Market (constant €)'] / 1e9
        
           

        else:
            st.error("The requested columns are not available in the filtered data.")

        # Filtrer uniquement les lignes nécessaires pour New et R&M pour Residential et Non-Residential
        filtered_data1 = filtered_data[
            (filtered_data['Activity type'].isin(['New', 'R&M'])) & 
            (filtered_data['Construction segment'].isin(['Residential', 'Non-Residential']))
        ]
        
        if not filtered_data1.empty:          
            # Graphique Market
            color_discrete_map = {
                'New': 'royalblue', #royalblue
                'R&M': 'skyblue'
            }
            fig_market = px.line(
                filtered_data1,
                x='Year',
                y='Market (constant €)',
                color='Activity type',
                line_dash='Construction segment',
                color_discrete_map=color_discrete_map,                
                labels={'Market (constant Billion €)': 'Market (Constant €)'},
                title='Construction Market Trends (Constant Bn €)'
            )
            fig_market.update_layout(legend={'x': 0.75, 'y': -0.9})       
            # Afficher toutes les années sur l'axe x
            fig_market.update_layout(
                xaxis=dict(
                    tickmode='linear',
                    tick0=int(filtered_data['Year'].min()),
                    dtick=1
                )
            )
            fig_market.for_each_annotation(lambda a: a.update(text=" ".join(a.text.split("=")[-1].split()[1:])))
            st.plotly_chart(fig_market, use_container_width=True)

            # Graphique Evolution en barres (histogramme)
            color_discrete_map = {
                'New': 'mediumblue', #royalblue
                'R&M': 'skyblue'
            }
            fig_evolution = px.bar(
                filtered_data1,
                x='Year',
                y='Evolution (%)',
                
                color='Activity type',
                facet_col='Construction segment',
                barmode='group',
                labels={'Evolution (%)': 'Evolution (%)'},
                title='Yearly Growth Rates of Construction Market (Y vs Y-1) (%)',
                color_discrete_map=color_discrete_map
            )
            # Suppression de l'en-tête de la facette ("Construction type")
            fig_evolution.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
            fig_evolution.update_xaxes(title_text='') #Supprimer 'Year' de l'axe x
            
            # Mise à jour de la mise en page pour déplacer les titres des axes
            fig_evolution.update_layout(
                xaxis_title='New = New construction. R&M = Renovation',
                xaxis_title_standoff=50,  # Ajuster la valeur pour déplacer le titre de l'axe X
                yaxis_title='Percentage Change (%)',
                yaxis_title_standoff=30   # Ajuster la valeur pour déplacer le titre de l'axe Y
            )
            # Afficher le graphique Evolution
            st.plotly_chart(fig_evolution, use_container_width=True)
            st.markdown('<script>window.scrollTo(0,0);</script>', unsafe_allow_html=True)

            
            if not filtered_data2.empty: 
                # Exclusion des lignes où Construction type est "All"
                filtered_data2 = filtered_data2[filtered_data2['Construction type'] != 'All']

            # Filtrer les options pour exclure 'Non-Residential'
            filtered_options = filtered_data2['Construction type'].unique()
            filtered_options = [option for option in filtered_options if option != 'Non-Residental - Type Not Defined']   

            selected_type= st.multiselect("Select building type to customize the chart below  ", options=filtered_options)

            if selected_type:
                # Pour le graphique, conservation des lignes où Activity type est New
                #filtered_data_graph = filtered_data2[(filtered_data2['Construction type'].isin(selected_type)) & (filtered_data2['Activity type'] == 'New')].copy()
                filtered_data_graph = filtered_data2[(filtered_data2['Construction type'].isin(selected_type)) & (filtered_data2['Activity type'] == 'New')].copy()
                
            else:
                
                filtered_data_graph = filtered_data_graph = filtered_data2[filtered_data2['Activity type'] == 'New'].copy()
                # Focus Evolution par type de bâtiment raphique Evolution en barres (histogramme)
                
                
            fig_evolution_type = px.bar(
                filtered_data_graph,
                x='Year',
                y='Evolution (%)',
                color='Activity type',
                facet_col='Construction type',
                barmode='group',
                labels={'Evolution (%)': 'Evolution (%)'},
                title='Yearly Growth Rates by type of building (Y vs Y-1) (%)',
                color_discrete_map=color_discrete_map
            )
            # Suppression de l'en-tête de la facette ("Construction type")
            fig_evolution_type.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
            # Mise à jour de la mise en page pour supprimer le titre de l'axe X
            fig_evolution_type.update_xaxes(title_text='') #Supprimer 'Year' de l'axe x

            # Afficher le graphique Evolution
            st.markdown('<script>window.scrollTo(0,0);</script>', unsafe_allow_html=True)
                      
            st.plotly_chart(fig_evolution_type, use_container_width=True)

            #Afficher les volumes marché (€) by Construction Type
            #if not filtered_data2.empty:
            fig_market2 = px.line(
                filtered_data_graph,    
                x='Year',
                y='Market (constant €)',                
                color='Construction type',
                #line_dash='Activity type',
                height=400,              
                labels={'Market (constant Billion €)': 'Market (Constant €)'},
                title='Construction Market trends by type of Non-Residential Building'
            )
            
            st.write("Nb : 'Others' includes agricultural buildings, hotels and restaurants, industrial and storage buildings, etc.")
            st.write("Nb : The type of Buildings is known for New Constructions only.")
            fig_market2.update_layout(
                    xaxis=dict(
                        tickvals=list(map(str, range(2019, 2027))),  # Liste des années à afficher
                        ticktext=list(map(str, range(2019, 2027))),  # Texte des ticks
                        tickmode='array',
                        title_standoff=20

                    )
            )
            fig_market2.update_xaxes(title_text='') #Supprimer 'Year' de l'axe x
            

            st.plotly_chart(fig_market2, use_container_width=True)
            #st.write("***Nb : 'Others' includes agricultural buildings, hotels and restaurants, industrial and storage buildings, etc***")
            st.markdown("<hr>", unsafe_allow_html=True) 
            

            # Afficher les données filtrées POUR LE PREMIER DATAFRAME
            st.write('**RELATED FILES**')
            st.write('**You can download them at your convenience :**')
            st.write('**1. Construction market by Construction segment (Non-Residential / Residential)**')
            #st.image("download.png", width=20) #:arrow_down_small:
            st.dataframe(filtered_data[['Country', 'Year', 'Activity type', 'Construction segment', \
                                    'Market (constant Billion €)', 'Evolution (%)']], use_container_width=True)
            
            st.write('**2. Construction market by Type of Non-Residential Building (Health, Education, etc.)**')
            # Afficher les données filtrées POUR LE DEUXIEME DATAFRAME
            # Correction de l'orthographe dans la colonne 'Construction type'
            filtered_data2.loc[
                filtered_data2['Construction type'] == 'Non-Residental - Type Not Defined', 
                'Construction type'
            ] = 'Non-Residential - Type Not Defined'
            
            st.dataframe(filtered_data2[['Country', 'Year', 'Activity type','Construction type', 'Market (constant Billion €)', 'Evolution (%)']], use_container_width=True)
            st.write("Nb : The type of Non-Residential Buildings renovated is not communicated by Euroconstruct")
            st.markdown("<hr>", unsafe_allow_html=True) 

            st.subheader("Further Market Information")
           

            # Afficher les sous-totaux
            selected_years = st.multiselect('Select a year to obtain further market information', options=filtered_data['Year'].unique())

            if selected_years:
                # Filtrer les données pour les années sélectionnées
                
                filtered_data_years = filtered_data[filtered_data['Year'].isin(selected_years)]
                filtered_data_years2 = filtered_data2[filtered_data2['Year'].isin(selected_years)]
                                
                # Sélectionner les lignes correspondantes pour chaque catégorie
                total_building = filtered_data_years[
                    (filtered_data_years['Activity type'] == 'New') | 
                    (filtered_data_years['Activity type'] == 'R&M')
                ]
                
                total_new_rm_residential = filtered_data_years[
                    (filtered_data_years['Activity type'].isin(['New', 'R&M'])) & 
                    (filtered_data_years['Construction segment'] == 'Residential')
                ]
                
                total_new_rm_non_residential = filtered_data_years[
                    (filtered_data_years['Activity type'].isin(['New', 'R&M'])) & 
                    (filtered_data_years['Construction segment'] == 'Non-Residential')
                ]

                

                # Construire le tableau des sous-totaux avec calculs pondérés # différences d'arrondies trop importantes parfois
                sous_total_table = {
                    "Total Market": [
                        total_building['Market (constant Billion €)'].sum() if not total_building.empty else 0
                        #weighted_avg(total_building, 'Market (constant Billion €)', 'Evolution (%)') if not total_building.empty else 0
                    ],
                    "Total New+R&M Residential": [
                        total_new_rm_residential['Market (constant Billion €)'].sum() if not total_new_rm_residential.empty else 0,
                        #weighted_avg(total_new_rm_residential, 'Market (constant Billion €)', 'Evolution (%)') if not total_new_rm_residential.empty else 0
                    ],
                    "Total New+R&M Non-Residential": [
                        total_new_rm_non_residential['Market (constant Billion €)'].sum() if not total_new_rm_non_residential.empty else 0,
                        #weighted_avg(total_new_rm_non_residential, 'Market (constant Billion €)', 'Evolution (%)') if not total_new_rm_non_residential.empty else 0
                    ]
                }
                    
                # Créer un DataFrame à partir des sous-totaux
                sous_total_df = pd.DataFrame(sous_total_table, index=["Bn €"])
                # Arrondir les valeurs en milliards à 2 décimales
                sous_total_df.loc["Bn €"] = sous_total_df.loc["Bn €"].apply(lambda x: round(x, 2))

                # Afficher le tableau des sous-totaux
                st.markdown(f'**Construction Market Subtotals for {", ".join(map(str, selected_years))}**')
                st.dataframe(sous_total_df, use_container_width=True)
               
                # Filtrer les données pour les années sélectionnées
            filtered_data_years = filtered_data1[filtered_data['Year'].isin(selected_years)]
           

            # Créer le pie chart Residential vs Non-Residential
            pie_data_rn = filtered_data_years.groupby('Construction segment')['Market (constant Billion €)'].sum()
            labels_rn = pie_data_rn.index
            values_rn = pie_data_rn.values
            colors_rn = ['red',' green']

            fig_pie_rn = go.Figure(data=[go.Pie(labels=labels_rn, values=values_rn, marker=dict(colors=colors_rn))])
            fig_pie_rn.update_layout(
                title=f'Construction Market by Construction segment for {", ".join(map(str, selected_years))}',
                font=dict(size=13), 
                legend={'x': 0.4, 'y': -0.2}

            )
            #Afficher les pie charts
            st.plotly_chart(fig_pie_rn, use_container_width=True)
          
            # Créer le pie chart New vs R&M
             # Créer le pie chart New vs R&M
            pie_data_new = filtered_data_years.groupby('Activity type')['Market (constant Billion €)'].sum()
            # Ordonner les données et les couleurs en conséquence
            #pie_data_nr = pie_data_nr.reindex(['R&M', 'New'])
            labels_new = pie_data_new.index
            values_new = pie_data_new.values
            #colors_nr = ['skyblue','deeproyalblue']
            colors_new = ['mediumblue','skyblue']  

            fig_pie_new = go.Figure(data=[go.Pie(labels=labels_new, values=values_new, marker=dict(colors=colors_new))])
            fig_pie_new.update_layout(
                title=f'Construction Market by Activity type for {", ".join(map(str, selected_years))}',
                font=dict(size=13),
                legend={'x': 0.4, 'y': -0.2}
            )
            st.plotly_chart(fig_pie_new, use_container_width=True)
            st. write("**Construction Market by activity type according to the Construction segment**")
            # Nouveau sélecteur pour le segment de construction
            #proposer l'option de personnaliser le grahique
            selected_segment = st.selectbox("Select Construction Segment", options=['Residential', 'Non-Residential'])

            # Filtrer les données en fonction du segment de construction sélectionné
            # Filtrer les données en fonction du segment de construction sélectionné et des années sélectionnées
            filtered_segment_data = filtered_data_years[filtered_data_years['Construction segment'] == selected_segment]

            # Regrouper les données par type d'activité ('New' vs 'R&M')
            pie_data_new2 = filtered_segment_data.groupby('Activity type')['Market (constant Billion €)'].sum()

            # Ordonner les données et les couleurs en conséquence
            #pie_data_nr = pie_data_nr.reindex(['R&M', 'New'])
            labels_new = pie_data_new2.index
            values_new = pie_data_new2.values
            #colors_nr = ['skyblue','deeproyalblue']
            colors_new = ['mediumblue','skyblue']  

            fig_pie_new2 = go.Figure(data=[go.Pie(labels=labels_new, values=values_new, marker=dict(colors=colors_new))])
            fig_pie_new2.update_layout(
                title=f'Construction Market by Activity type for {selected_segment} Market for {", ".join(map(str, selected_years))}',
                font=dict(size=13),
                legend={'x': 0.4, 'y': -0.2}
            )
            
            st.plotly_chart(fig_pie_new2, use_container_width=True)

               
        else:
            st.warning("Please select at least one year to display the pie charts.")
    # else:
    #     st.warning("Aucune donnée disponible pour les filtres sélectionnés.")
    
        if selected_years:
            filtered_data2_years = filtered_data2[filtered_data2['Year'].isin(selected_years)]
            
            # Agrégation des données par type de construction
            # Exclusion des lignes où Construction type est "All"
            filtered_data2_years = filtered_data2_years[filtered_data2_years['Construction type'] != 'All']
            # Conservation des lignes où Activity type est New
            filtered_data2_years = filtered_data2_years[filtered_data2_years['Activity type'] == 'New']
            pie_data = filtered_data2_years.groupby('Construction type')['Market (constant Billion €)'].sum().reset_index()
            
            # Création du pie chart
            fig_pie = px.pie(
                pie_data,
                names='Construction type',
                values='Market (constant Billion €)',
                title=f'Construction Market Breakdown by Type of Non-Residential Buildings for {", ".join(map(str, selected_years))}'
            )
            
            # Personnalisation du graphique
            fig_pie.update_traces(textinfo='label+percent', 
                        texttemplate='%{label} <br> %{percent:.1%}')
            fig_pie.update_layout(
                showlegend=False,     
            #     legend={'x': 0.4, 'y': -0.7}
            )
            
            # Affichage du graphique
            st.plotly_chart(fig_pie, use_container_width=True)
            st.write("'Others' includes agricultural buildings, hotels and restaurants, industrial and storage buildings, ...")
            
            #st.image("download.png", width=20) #:arrow_down_small:

            # Afficher les données filtrées POUR LE PREMIER DATAFRAME
            st.markdown("<hr>", unsafe_allow_html=True)
            st.write(f'**RELATED FILES FOR {", ".join(map(str, selected_years))}**')
            st.write('**1. Construction market by Construction segment (Non-Residential / Residential)**')
            
            st.dataframe(filtered_data_years[['Country', 'Year', 'Activity type', 'Construction segment',
                                    'Market (constant Billion €)', 'Evolution (%)']], use_container_width=True, hide_index=True)
            st.write('**2. Construction market by Type of Non-Residential Building (Health, Education, etc.)**')
            # Afficher les données filtrées POUR LE DEUXIEME DATAFRAME
            # Correction de l'orthographe dans la colonne 'Construction type'
            filtered_data2_years.loc[
                filtered_data2_years['Construction type'] == 'Non-Residental - Type Not Defined', 
                'Construction type'
            ] = 'Non-Residential - Type Not Defined'
            
            
            st.dataframe(filtered_data2_years[['Country', 'Year', 'Activity type','Construction type', 'Market (constant Billion €)', 'Evolution (%)']], \
                         use_container_width=True, hide_index=True)
            st.write("Nb : The type of Non-Residential Buildings renovated is not communicated by Euroconstruct")
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### Appendix", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
            # Current path
        st.image("methodo.png", use_column_width=True)
        # Ajouter un bouton pour télécharger l'image
        with open("methodo.png", "rb") as file:
            st.download_button(label="Download Methodology image", data=file, file_name="methodo.png", mime="image/png")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<script>window.scrollTo(0,0);</script>', unsafe_allow_html=True)
        st.image("learnings.png", use_column_width=True)
        # Ajouter un bouton pour télécharger l'image
        with open("learnings.png", "rb") as file:
            st.download_button(label="Download key learnings", data=file, file_name="learnings.png", mime="image/png")
        st.markdown("<hr>", unsafe_allow_html=True)
        st.success("End of this page.")
        
        
    elif choix == "HVAC market":
            data3 = pd.read_excel("Ventilation_trends.xlsx")
            
            data4 = pd.read_excel("HVAC_market.xlsx")           
            
            
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("### Page 2 - HVAC Market", unsafe_allow_html=True)
            st.markdown("_Main sources : Euroconstruct 2024 Summer edition, Eurovent July 2024, BSRIA April 2024_")
            st.markdown("<hr>", unsafe_allow_html=True)
            
    
            # Current path
            st.image("HVAC market.png", use_column_width=True)
            # Ajouter un bouton pour télécharger l'image
            with open("HVAC market.png", "rb") as file:
                st.download_button(label="Download HVAC market image", data=file, file_name="HVAC_market.png", mime="image/png")
            
            st.markdown('<script>window.scrollTo(0,0);</script>', unsafe_allow_html=True)
            st.image("eurovent.png", use_column_width=True)
            # Ajouter un bouton pour télécharger l'image
            with open("eurovent.png", "rb") as file:
                st.download_button(label="Download Eurovent image", data=file, file_name="eurovent.png", mime="image/png")

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<script>window.scrollTo(0,0);</script>', unsafe_allow_html=True)
            st.markdown("### 2024-2025 Ventilation & HRU Market trends by country", unsafe_allow_html=True)
            st.write("_Sources : Eurovent, Euroconstruct_")
            st.write("**Yearly trends in % (Y vs Y-1). Main application : Non-Residential**")
            

            # Sélection des filtres
            selected_countries2 = st.multiselect('Select the country', options=data3['Country'].unique())
            # Filtrer les données en fonction des filtres sélectionnés
            if selected_countries2:
                filtered_data3 = data3[data3['Country'].isin(selected_countries2)].copy()
                filtered_data4 = data4[data4['Country'].isin(selected_countries2)].copy()
               
            else:
                filtered_data3 = data3.copy()
                filtered_data4 = data4.copy()
            # Ajouter un "%" aux modalités des colonnes 2024 et 2025

            # Convertir tous les noms de colonnes en chaînes de caractères
            filtered_data3.columns = filtered_data3.columns.map(str)
            
            if '2024' in filtered_data3.columns and '2025' in filtered_data3.columns:
                filtered_data3["2024"] = filtered_data3["2024"].apply(lambda x:f"{round(x, 1)}%")
                filtered_data3["2025"] = filtered_data3["2025"].apply(lambda x: f"{round(x, 1)}%")
            st.dataframe(filtered_data3, use_container_width=True)

            
            # Générer le graphique en barres avec Plotly
            fig5 = go.Figure(data=[
                go.Bar(name='2024', x=filtered_data3['Country'], y=filtered_data3['2024'], marker_color='orange'),
                go.Bar(name='2025', x=filtered_data3['Country'], y=filtered_data3['2025'], marker_color='darkblue')
            ])

            # Mettre à jour la mise en page pour ajuster les étiquettes de l'axe x
            fig5.update_layout(
                title='2024 & 2025 Ventilation & HRU Market trends by country (Main application : Non-Residential)',
                #xaxis_title='Country',
                yaxis_title='Percentage Change (%)',
                barmode='group',
                xaxis_tickangle=-45
            )

            # Afficher le graphique dans Streamlit
            st.plotly_chart(fig5)



            #Fonction de conversion des coefficients en pourcentage
            if 'Market evolution in units' in filtered_data4.columns:
                filtered_data4["Market evolution in units"] = \
                filtered_data4["Market evolution in units"].apply(lambda x: f"{round((x - 1) * 100, 1)}%")
                filtered_data4["Market evolution in value (€)"] = \
                filtered_data4["Market evolution in value (€)"].apply(lambda x: f"{round((x - 1) * 100, 1)}%")
                filtered_data4["Avg selling price (€)"] = filtered_data4["Avg selling price (€)"].apply(lambda x: round(x, 0))

            filtered_data4['Year'] = filtered_data4['Year'].astype(str)

            st.markdown("<hr>", unsafe_allow_html=True)            
            st.markdown('<script>window.scrollTo(0,0);</script>', unsafe_allow_html=True)
            st.markdown("### 2023 Ventilation & HRU Markets", unsafe_allow_html=True)
            
           

            # Filtrer les données pour la ventilation uniquement
            ventilation_data = filtered_data4[filtered_data4['HVAC Typology'] == 'VENTILATION']

            # Calculer le volume du marché total par application principale du bâtiment et par nom de produit
            market_volume_by_app_division = ventilation_data.groupby(['Main Building Application', 'Division'])['Market volume (€)'].sum().reset_index()

            # Générer le graphique en barres empilées pour le volume du marché par application principale du bâtiment et par nom de produit
            fig_ventilation = go.Figure()

            for division in market_volume_by_app_division['Division'].unique():
                product_data = market_volume_by_app_division[market_volume_by_app_division['Division'] == division]
                fig_ventilation.add_trace(go.Bar(
                    name=division,
                    x=product_data['Main Building Application'],
                    y=product_data['Market volume (€)']
                ))

            fig_ventilation.update_layout(
                title=f'2023 Market Volumes (€) by Main Building Application and Division for {", ".join(map(str, selected_countries2))}',
    
                xaxis_title='Main Building Application. NR = Non-Residential. RES = Residential',
                yaxis_title='Market Volume (€)',
                barmode='stack',
                xaxis_tickangle=-45, 
                               
            )

            st.plotly_chart(fig_ventilation)

            # Générer le graphique en barres empilées pour le volume du marché par application principale du bâtiment et par nom de produit
            # Calculer le volume du marché total par application principale du bâtiment et par nom de produit
            market_volume_by_app_product = ventilation_data.groupby(['Main Building Application', 'Product Name'])['Market volume (€)'].sum().reset_index()
            fig_ventilation2 = go.Figure()

            for product in market_volume_by_app_product['Product Name'].unique():
                product_data = market_volume_by_app_product[market_volume_by_app_product['Product Name'] == product]
                fig_ventilation2.add_trace(go.Bar(
                    name=product,
                    x=product_data['Main Building Application'],
                    y=product_data['Market volume (€)']
                ))

            fig_ventilation2.update_layout(
                title=f'2023 Market Volumes (€) by Main Building Application and Product Name for {", ".join(map(str, selected_countries2))}',
                xaxis_title='Main Building Application. NR = Non-Residential. RES = Residential',
                yaxis_title='Market Volume (€)',
                barmode='stack',
                xaxis_tickangle=-45, 
                               
            )

            st.plotly_chart(fig_ventilation2)

            st.markdown("<hr>", unsafe_allow_html=True)            
            st.markdown('<script>window.scrollTo(0,0);</script>', unsafe_allow_html=True)
            st.markdown("### 2023 Heating & Air conditioning Markets", unsafe_allow_html=True)
            st.write('On a range of products for which we have recent information')

            # Filtrer les données pour Heating & air conditioning
            airco_data = filtered_data4[filtered_data4['HVAC Typology'] == 'HEATING & AIR CONDITIONING']

             # Calculer le volume du marché total par application principale du bâtiment et par nom de produit
            market_volume_by_airco = airco_data.groupby(['Main Building Application', 'Product Name'])['Market volume (€)'].sum().reset_index()

            fig_airco = go.Figure()

            for product in market_volume_by_airco['Product Name'].unique():
                product_data = market_volume_by_airco[market_volume_by_airco['Product Name'] == product]
                fig_airco.add_trace(go.Bar(
                    name=product,
                    x=product_data['Main Building Application'],
                    y=product_data['Market volume (€)']
                ))

            fig_airco.update_layout(
                title=f'2023 Market Volumes (€) by Main Building Application and Product Name for {", ".join(map(str, selected_countries2))}',
                xaxis_title='Main Building Application. NR = Non-Residential. RES = Residential',
                yaxis_title='Market Volume (€)',
                barmode='stack',
                xaxis_tickangle=-45, 
                               
            )

            st.plotly_chart(fig_airco)
           
            st.markdown('<script>window.scrollTo(0,0);</script>', unsafe_allow_html=True)
            st.markdown('<script>window.scrollTo(0,0);</script>', unsafe_allow_html=True)
            st.markdown('<script>window.scrollTo(0,0);</script>', unsafe_allow_html=True)
            
            st.markdown("### 2023 HVAC Market - Eurovent & EHPA Collections", unsafe_allow_html=True)
            st.write("**You can download the file at your convenience.**")
                       
             
            # Sélection des filtres Produit
            excluded_products = ['Diffusors & Grilles', 'Car park smoke Exhaust fans', 'Central SF 1000-2500m3/h',\
                                 'Central SF 250-1000m3/h', 'SF Central VU', 'Fixings', \
                                 'Ducts in km', 'Non residential Air valves', 'Residential Air Inlets',\
                                 'VAV valves', 'Diffusors & Grilles','Fire dampers', 'Natural Smoke Exhaust System',\
                                 'Residential Air valves', 'Smoke dampers'
                                 
            ]
            ## Obtenir les noms de produits uniques à partir des données
            all_products = filtered_data4['Product Name'].unique()

            # Filtrer les options pour exclure les produits spécifiés
            filtered_options = [product for product in all_products if product not in excluded_products]

            # Créer un multiselect avec les options filtrées
            selected_product = st.multiselect('Select the product', options=filtered_options)
           
            # Filtrer les données en fonction des filtres sélectionnés
            if selected_product:
                filtered_data4 = filtered_data4[filtered_data4['Product Name'].isin(selected_product)].copy()
               
            else:
                filtered_data4 = filtered_data4[~filtered_data4['Product Name'].isin(excluded_products)].copy()
            
            
            st.dataframe(filtered_data4[['Country', 'Year', 'HVAC Typology', \
                                    'Product Name', 'Units sold (qty)', 'Avg selling price (€)', 'Market volume (€)',\
                                    'Market evolution in units', 'Market evolution in value (€)', 'Source']], use_container_width=True)
            
            
            
            st.markdown("<hr>", unsafe_allow_html=True)
            st.success("End of this page.")   


# Streamlit main function call
if __name__ == "__main__":
    main()

