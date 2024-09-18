import pandas as pd

def Populating_mpmb_df():
    # This function should return the dataframe. For demonstration, I'm creating a sample dataframe.
    data = {'d/u': [10, 15, 14, 19, 20, 21, 22, 25, 18, 12, 8, 17]}
    df = pd.DataFrame(data)
    return df

def calc_table():
    df = Populating_mpmb_df()

    # Count and calculate percentages
    total_values = df["d/u"].count()
    count_below_16 = df["d/u"][df["d/u"] < 16].count()
    percentage_below_16 = (count_below_16 / total_values) * 100

    count_below_20 = df["d/u"][df["d/u"] < 20].count()
    percentage_below_20 = (count_below_20 / total_values) * 100

    count_eqgt_20 = df["d/u"][df["d/u"] >= 20].count()
    percentage_eqgt_20 = (count_eqgt_20 / total_values) * 100

    # Generate HTML table
    table = f"""
    <table border="1" style="width:50%; border-collapse: collapse; text-align: center;">
        <thead>
            <tr>
                <th>Description</th>
                <th>Percentage</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Percentage of d/u values &lt; 16</td>
                <td>{percentage_below_16:.2f}%</td>
            </tr>
            <tr>
                <td>Percentage of d/u values &lt; 20</td>
                <td>{percentage_below_20:.2f}%</td>
            </tr>
            <tr>
                <td>Percentage of d/u values &gt;= 20</td>
                <td>{percentage_eqgt_20:.2f}%</td>
            </tr>
        </tbody>
    </table>
    """

    print(table)
    return table

# Call the function to generate and print the HTML table
calc_table()
