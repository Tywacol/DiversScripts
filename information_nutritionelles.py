import pandas as pd

sheets = []

with pd.ExcelFile("/home/ccalleri/Documents/Charlotte/AutomtisationInfosNutritionelles/données nutritionnelles.ods") as xls:
    print(xls.sheet_names)
    sheets = xls.sheet_names
    dfs = [pd.read_excel(xls, sheet_name, engine="odf") for sheet_name in xls.sheet_names]
    donnees_nutritionnelles = pd.read_excel(xls, sheet_name="Données nutritionnelles", engine="odf")

    ingredients_by_recettes_ordered = []

    total_nutrition_by_recette = {
        'Énergie (kJ)' : [],
        'Energie (kcal)' : [],
        'Matières grasses (g)': [],
        'dont acides gras saturés (g)' : [],
        'Glucides (g)' : [],
        'dont sucres (g)' : [],
        'Protéines (g)' : [],
        'Sel (g)' : []
    }

    for df, sheet in zip(dfs, xls.sheet_names) :
        if sheet not in('Données nutritionnelles', 'Total') : 
            df = df.sort_values(by=["masse (g)"], ascending=False)
            ingredients = ','.join(df["Ingrédients"])
            ingredients_by_recettes_ordered.append(ingredients)
            df["Liste des ingrédients"]= ""
            df.loc[[0],"Liste des ingrédients"] = ingredients

            total_nutrition = {
                'Énergie (kJ)' : 0,
                'Energie (kcal)' : 0,
                'Matières grasses (g)': 0,
                'dont acides gras saturés (g)' : 0,
                'Glucides (g)' : 0,
                'dont sucres (g)' : 0,
                'Protéines (g)' : 0,
                'Sel (g)' : 0
            }
            # Pour chaque ingredient et pour chaque masse associée 
            # Multiplier l'ensemble des caracteristique nutritionnelles de l'ingredient par la quantité d'ingrédient dans 100g de produit
            # ajouter l'ensemble au caracteristiques nutritionelles de la recette"""
            for ingredient,masse in zip(df.Ingrédients, df['masse (g)']) :
                ingredient_nutrition = donnees_nutritionnelles[donnees_nutritionnelles['Pour 100g'] == ingredient]
                if ingredient_nutrition.empty :
                    print(f"Ingredient not found: {ingredient} in: {sheet}")
                else :
                    for carac in total_nutrition :
                        proportion = masse / df['masse (g)'].sum()
                        total_nutrition[carac] += ingredient_nutrition.iloc[0][carac] * proportion
            for carac in total_nutrition_by_recette :
                total_nutrition_by_recette[carac].append(total_nutrition[carac])


    total_df = pd.DataFrame(
        {'Recette': xls.sheet_names[1:-1], 
         'Ingredients ordonnés' : ingredients_by_recettes_ordered
        } | total_nutrition_by_recette # dictionnary merge python >3.9
    )

    writer = pd.ExcelWriter("/home/ccalleri/Documents/Charlotte/AutomtisationInfosNutritionelles/données nutritionnelles.ods", engine='odf')
    for df,sheet in zip(dfs,sheets):
        if sheet != 'Total' :
            df.to_excel(writer, sheet_name=sheet, index=False)
    total_df.to_excel(writer, sheet_name='Total', index=False)
    
    writer.save()
    writer.close()
        

