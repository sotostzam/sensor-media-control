import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import glob
import os
import datetime as dt

def find_average(start, end):
    diff = start - end
    change = diff / start * 100
    return (start, end, change)

def generate():
    file_list = glob.glob('./experiments/*.csv')
    main_dataframe = pd.DataFrame(pd.read_csv(file_list[0]))
    main_dataframe.insert(2,'Date',os.path.basename(file_list[0])[:8])
    main_dataframe.insert(2,'Timestamp',os.path.basename(file_list[0])[8:14])
    for i in range(1,len(file_list)):
        data = pd.read_csv(file_list[i])
        data.insert(2,'Date',os.path.basename(file_list[i])[:8])
        data.insert(2,'Timestamp',os.path.basename(file_list[i])[8:14])
        df = pd.DataFrame(data)
        main_dataframe = pd.concat([main_dataframe,df],axis=0)

    # Populating the data
    dates = sorted(set(main_dataframe["Date"].to_numpy()))
    x_values = list(dt.datetime.strptime(str(d),'%Y%m%d').date() for d in dates)

    y_values_sl = []
    y_values_sr = []
    y_values_il = []
    y_values_ir = []

    correct_sl = []
    correct_sr = []
    correct_il = []
    correct_ir = []

    averages = []

    for date in dates:
        average_speed_per_day = []

        # Get the speed values of the tests for each date
        time = main_dataframe[(main_dataframe['Date']==date) & main_dataframe['Correct']==True]
        y_values_sl.append(time['Time'][(time['Mode']=='speed') & (time['Tab']=='layout')].to_numpy())
        y_values_sr.append(time['Time'][(time['Mode']=='speed') & (time['Tab']=='remote')].to_numpy())
        y_values_il.append(time['Time'][(time['Mode']=='interactive') & (time['Tab']=='layout')].to_numpy())
        y_values_ir.append(time['Time'][(time['Mode']=='interactive') & (time['Tab']=='remote')].to_numpy())

        average_speed_per_day.append(np.average(time['Time'][(time['Mode']=='speed') & (time['Tab']=='layout')].to_numpy()))
        average_speed_per_day.append(np.average(time['Time'][(time['Mode']=='interactive') & (time['Tab']=='layout')].to_numpy()))
        average_speed_per_day.append(np.average(time['Time'][(time['Mode']=='speed') & (time['Tab']=='remote')].to_numpy()))
        average_speed_per_day.append(np.average(time['Time'][(time['Mode']=='interactive') & (time['Tab']=='remote')].to_numpy()))

        averages.append(average_speed_per_day)

        # Get the average amount of results for each date
        tests_num = len(set(time["Timestamp"].to_numpy()))
        correct_sl.append(round(len(time[(time['Mode']=='speed') & (time['Tab']=='layout')].to_numpy())/tests_num))
        correct_sr.append(round(len(time[(time['Mode']=='speed') & (time['Tab']=='remote')].to_numpy())/tests_num))
        correct_il.append(round(len(time[(time['Mode']=='interactive') & (time['Tab']=='layout')].to_numpy())/tests_num))
        correct_ir.append(round(len(time[(time['Mode']=='interactive') & (time['Tab']=='remote')].to_numpy())/tests_num))

    # Identify which part of the screen has the most mistakes
    screen_left  = ['Stop', 'Play/Pause']
    screen_right = ['Volume', 'Mute']
    screen_upper = ['OK', 'ESC', 'Previous', 'Next']

    layout_experiments_mistakes = main_dataframe[(main_dataframe['Tab']=='layout') & (main_dataframe['Correct'] == False)]
    layout_experiments_mistakes = layout_experiments_mistakes['Required Action'].value_counts()
    screen_left_total = screen_right_total = screen_upper_total = screen_lower_total = 0
    for i in range(0, len(layout_experiments_mistakes.index)):
        if layout_experiments_mistakes.index[i] in screen_left:
            screen_left_total+=layout_experiments_mistakes.values[i]
        elif layout_experiments_mistakes.index[i] in screen_right:
            screen_right_total+=layout_experiments_mistakes.values[i]
        elif layout_experiments_mistakes.index[i] in screen_upper:
            screen_upper_total+=layout_experiments_mistakes.values[i]
        else:
            screen_lower_total+=layout_experiments_mistakes.values[i]
    
    # Populate averages (mean) and percentage increase for each test
    average_layout_speed = find_average(averages[0][0], averages[-1][0])
    average_layout_inter = find_average(averages[0][1], averages[-1][1])
    average_remote_speed = find_average(averages[0][2], averages[-1][2])
    average_remote_inter = find_average(averages[0][3], averages[-1][3])

    # Create figure for all the speed values as boxplots
    fig = plt.figure(1, figsize=(12, 8))
    axs = fig.subplots(2, 2)
    axs[0, 0].boxplot(y_values_sl, labels=x_values, showmeans=True)
    axs[0, 0].set_title('Speed Mode - Layout')
    axs[0, 1].boxplot(y_values_sr, labels=x_values, showmeans=True)
    axs[0, 1].set_title('Speed Mode - Remote')
    axs[1, 0].boxplot(y_values_il, labels=x_values, showmeans=True)
    axs[1, 0].set_title('Interactive Mode - Layout')
    axs[1, 1].boxplot(y_values_ir, labels=x_values, showmeans=True)
    axs[1, 1].set_title('Interactive Mode - Remote')

    for ax in fig.get_axes():
        ax.label_outer()
        ax.set_ylim(0, 5)

    # Create figure for correct answers per day as a lineplot
    fig2 = plt.figure(2, figsize=(7, 6))
    ax2 = fig2.add_subplot(111)
    ax2.plot(x_values, correct_sl, label="Speed-Layout")
    ax2.plot(x_values, correct_sr, label="Speed-Remote")
    ax2.plot(x_values, correct_il, label="Interactive-Layout")
    ax2.plot(x_values, correct_ir, label="Interactive-Remote")

    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax2.legend()

    # Create figure for the percentage of speed increase through memory
    fig3 = plt.figure(3, figsize=(7, 6))
    ax3 = fig3.add_subplot(111)

    labels = ['Layout-Speed', 'Layout-Interactive', 'Remote-Speed', 'Remote-Interactive']
    width = 0.40
    x = np.arange(len(labels))

    ax3.bar(x - width/2, [average_layout_speed[0], average_layout_inter[0], average_remote_speed[0], average_remote_inter[0]], width, label='Start')
    diffs = ax3.bar(x + width/2, [average_layout_speed[1], average_layout_inter[1], average_remote_speed[1], average_remote_inter[1]], width, label='End')

    ax3.bar_label(diffs, padding=3, labels=[('-' + str(round(average_layout_speed[2], 1)) + '%'),
                                            ('-' + str(round(average_layout_inter[2], 1)) + '%'),
                                            ('-' + str(round(average_remote_speed[2], 1)) + '%'),
                                            ('-' + str(round(average_remote_inter[2], 1)) + '%')])

    ax3.set_ylabel('Time (sec)')
    ax3.set_title('Average Time at the start and end of the experiments')
    ax3.set_xticks(x, labels)
    ax3.legend()

    # Show the most frequent mistakes
    fig4 = plt.figure(4, figsize=(7, 6))
    axs4 = fig4.subplots(2, 1)
    axs4[0].bar(layout_experiments_mistakes.index, layout_experiments_mistakes.values)
    axs4[0].set_title('Mistakes per interaction')
    axs4[1].bar(['Left', 'Right', 'Upper', 'Lower'], [screen_left_total, screen_right_total, screen_upper_total, screen_lower_total])
    axs4[1].set_title('Mistakes per part of the screen')

    plt.show()

if __name__ == "__main__":
    generate()