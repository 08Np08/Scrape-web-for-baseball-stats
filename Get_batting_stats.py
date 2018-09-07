import pandas as pd
import pickle

END_YEAR= int(input("Enter the end year:")

START_YEAR = int("Enter the start year:")
              
YEARS = START_YEAR - END_YEAR

file = open("batting stats.pickle","wb")

def main():
    
    COLUMNS = ["Rk","Gcar","Opp","AB","R","H","2B","3B",
           "HR","RBI","BB","IBB",'SO',"HBP","SB","CS",
           "OBP","SLG","OPS","BOP","aLI","WPA","RE24"]

    batter_DF = pd.DataFrame(columns = COLUMNS)

    count = 0
    
    batters_dict = {}
    batters = get_batters("batters.csv")

    
    for i in range(len(batters)):
        for j in range(YEARS):
            try:
                count+=1
                
                batter = batters[i]
                
                batter_url = ("https://www.baseball-reference.com/players/gl.fcgi?id="
                              +batter+"&t=b&year="+str(START_YEAR + j))
            
                batter_list = pd.DataFrame(pd.read_html(batter_url)[4])

                drop_rows_by_equals(batter_list,"AB","R")
    
                drop_rows_by_equals(batter_list,"Gcar","Gtm")
    
                drop_rows_by_greater(batter_list,"AB",10)
                
                batter_DF = batter_DF.append(batter_list)
                
                print("Percent Finished:",round(count/
                      (YEARS*len(batters))*100,2),"%")
                
            except Exception as e:
                print(e)
                continue

                
        batters_dict[batter] = batter_DF
        batter_DF = pd.DataFrame(columns = COLUMNS)

    pickle.dump(batters_dict,file) 
    
def get_batters(csv):
    batters = pd.DataFrame(pd.read_csv(csv,sep=" "))
    batters = list(batters.astype(str).values.flatten())
    return(batters)
    
def drop_rows_by_equals(df,column,drop_criteria): 
    for i in range(len(df)):
        try:
            if df.iloc[i][column] == drop_criteria:
                df.drop(df.index[i], inplace=True)      
        except:
            continue
        
def drop_rows_by_greater(df,column,drop_criteria): 
    for i in range(len(df)):
        try:
            if int(df.iloc[i][column]) > drop_criteria:
                df.drop(df.index[i], inplace=True)     
        except:
            continue  
main()
