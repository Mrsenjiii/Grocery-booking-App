import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend (e.g., 'Agg')

df = None  # dataframe


def set_frame(sql_data):
    data = []

    for x in sql_data:
        data.append({
            'product_id':x.product_id,
            'product_name': x.product_name,
            'product_quantity': x.sold_items,
            'sold_date': x.sold_date,
            'product_price': x.product_price,
            'product_category': x.product_category
        })
    global df
    # print(len(data))
    df = pd.DataFrame(data)

    return "done sucessfully"
# Product_name product_quantity sold_date  product_price product_category ------> dataframe columns




def Sales_time_line_chart():
    df['sold_date'] = pd.to_datetime(df['sold_date'])
    df['product_price'] = pd.to_numeric(df['product_price'])
    df['product_quantity'] = pd.to_numeric(df['product_quantity'])
    df['total_sales'] = df['product_price']*df['product_quantity']

    daily_sales = df.groupby('sold_date')['total_sales'].sum().reset_index()
    # print(daily_sales['total_sales'])
    print(type(daily_sales.index))
    print(type(daily_sales.values))

    plt.figure(figsize=(12, 6))  # Set the figure size before plotting
    # print(daily_sales)
    plt.plot(daily_sales['sold_date'], daily_sales['total_sales'])
    plt.xlabel('Time in days')
    plt.ylabel('Total Sales in ₹')
    plt.title('Time Vs Sales')
    plt.xticks(rotation=0)
    plt.tight_layout()
    # plt.savefig('static/amount_of_product_sold_vs_time.png')
    plt.close()




def month_wise_analysis():
    newdf = df.loc[:, ['sold_date', 'product_price', 'product_quantity']]
    newdf['product_price'] = pd.to_numeric(newdf['product_price'])
    newdf['product_quantity'] = pd.to_numeric(newdf['product_quantity'])
    newdf['total_sold'] = newdf['product_price'] *  newdf['product_quantity']  # new column
    newdf['sold_date'] = pd.to_datetime(newdf['sold_date'])
    # Create a new 'Month' column with the month information
    newdf['Month'] = newdf['sold_date'].dt.to_period('M')
    monthly_analysis = newdf.groupby('Month')['total_sold'].sum()
    # print(monthly_analysis)
    monthly_analysis.index = monthly_analysis.index.strftime('%B-%Y')
    # print(monthly_analysis.index)
    plt.figure(figsize=(6, 4))
    plt.bar(monthly_analysis.index, monthly_analysis.values, width=0.5)
    plt.xlabel('Month')
    plt.ylabel('Total Sales in Rupee')
    plt.title('Total Sales vs. Month')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    # plt.savefig('static/month_wise_sales.png')
    # plt.show()
    plt.close()
    return None


def Category_wise_analysis():
    category = df['product_category'].unique()
    # print(category)
    for cate in category : 
        filt = (df['product_category'] == cate)
        # print(filt)
        required_data = df.loc[filt, ['product_name', 'product_price']]
        grouped_data = required_data.groupby(
            'product_name')['product_price'].sum()
        
        plt.figure(figsize=(6, 4))
        plt.bar(grouped_data.index, grouped_data
                .values, width=0.5)
        plt.xlabel('Product')
        plt.ylabel('Sales')
        plt.title('Total Sales vs. Product')
        plt.xticks(rotation=0, ha='right')
        plt.tight_layout()
        path = f"static/analysis_of_{cate}_category.png"
        plt.savefig(path)
        plt.close()
        # plt.show()
    return None


def Category_pie_chart():
    df['product_price'] = pd.to_numeric(df['product_price'], errors='coerce')
    # Group by 'product_category' and sum the 'product_price' for each category
    category = df.groupby(df['product_category'])['product_price'].sum()
    print(category)
    # Plot the pie chart
    plt.figure(figsize=(6, 4))
    # category.plot(kind='pie', autopct='%1.1f%%')
    plt.pie(category.values,labels = category.index , autopct='%1.1f%%')
    plt.title('Total Sales by Category')
    plt.ylabel('')
    plt.savefig('static/Category_pie.png')
    plt.close()
    return None


def runner():
    Sales_time_line_chart()
    month_wise_analysis()
    Category_pie_chart()
    Category_wise_analysis()