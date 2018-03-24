#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 00:49:15 2018
@author: Nik
"""

import pandas as pd

YEARS = 1

START_YEAR = 2017

COLUMNS = ["Rk","Gcar","Opp","AB","R","H","2B","3B",
           "HR","RBI","BB","IBB",'SO',"HBP","SB","CS",
           "OBP","SLG","OPS","BOP","aLI","WPA","RE24"]

def main():
 
    count = 0
    batters_list = pd.DataFrame(columns = COLUMNS)
    batters = get_batters("batters.csv")
    
    for i in range(len(batters)):
        for j in range(YEARS):
            try:
                count+=1
                
                batter = batters[i]
                
                batter_url = ("https://www.baseball-reference.com/players/gl.fcgi?id="
                              +batter+"&t=b&year="+str(START_YEAR-j))
            
                batter_list = pd.DataFrame(pd.read_html(batter_url)[4])
                
                batter_list = batter_list[["Rk","Gcar","Gtm","Date","Tm",
                                           "Opp","Rslt","Inngs","PA",
                                           "AB","R","H","2B","3B","HR",
                                           "RBI","BB","IBB",'SO',"HBP",
                                           "SH","SF","ROE","GDP","SB",
                                           "CS","OBP","SLG","OPS","BOP",
                                           "aLI","WPA","RE24","DFS(DK)",
                                           "DFS(FD)",'Pos']]
            
                batter_list = batter_list.drop(batter_list.columns[[2,3,4,6,7,8,
                                                                    20,21,22,23,
                                                                    -1,-2,-3]],
                                                                    axis=1)
            
                batters_list = batters_list.append(batter_list)
                
                print("percent finished",round(count/
                      (YEARS*len(batters))*100,2),"%")
        
            except:
                print("error")
                continue
    
    drop_rows_by_equals(batters_list,"AB","R")
    
    drop_rows_by_equals(batters_list,"Gcar","Gtm")
    
    drop_rows_by_greater(batters_list,"AB",10)
    
    batters_list = batters_list.dropna(how="any", inplace = False)
    print(batters_list.shape)
    batters_list.to_pickle("batters_list")
    
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
