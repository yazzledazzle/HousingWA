import pandas as pd
from Waitlist_data import *
from Waitlist_latest_report import *
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_TABLE_DIRECTION, WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.enum.text import WD_ALIGN_PARAGRAPH



Waitlist_latest_report, Waitlist_latest_report_pc_pt, Waitlist_latest_report_full = Create_waitlist_latest_reports()

def notes_titles(df):
    df = df.dropna(axis=1, how='all')
    note_columns = [col for col in df.columns if 'Note' in col]
    df['Notes'] = df[note_columns].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)
    #drop note columns
    df = df.drop(columns=note_columns)
    R1C1 = {}
    label_keys = {'Total': 'label', 'Priority': 'plabel'}
    for group, label in label_keys.items():
        labeldf = df[df['Group'] == group]
        unique_dates = labeldf['Date'].unique()
        if len(unique_dates) == 1:
            date = unique_dates[0]
            R1C1[label] = f'At {date}'
            date = pd.to_datetime(date)
            date = date.strftime('%Y-%m-%d')
            continue
        else:
            R1C1[label] = ''
            labeldf['Date'] = pd.to_datetime(df['Date'])
            date = labeldf['Date'].max()
            date = date.strftime('%Y-%m-%d')
            df[R1C1[label]] = df['Count'] + ' - at ' + df['Date']


    total = df[df['Group'] == 'Total']
    priority = df[df['Group'] == 'Priority']
    total = total.drop(columns=['Group'])
    priority = priority.drop(columns=['Group'])
    total = total.reset_index(drop=True)
    priority = priority.reset_index(drop=True)
      
    print(R1C1)

    return total, priority, R1C1, date

def report_update(total, priority, R1C1, date):

    document = Document('assets/Report.docx')
    labels_dict = {'date': R1C1['label'],
                   'a_label': total['Count'][0], 
                   'i_label': total['Count'][1],
                   'a': total['#'][0],
                   'i': total['#'][1],
                   'pdate': R1C1['plabel'],
                   'pa_label': priority['Count'][0],
                   'pi_label': priority['Count'][1],
                   'pa': priority['#'][0],
                   'pi': priority['#'][1],
                }

    variables_dict = {
        'a_mc': total[total['Count'] == labels_dict['a_label']]['Prior month'].values[0],
        'i_mc': total[total['Count'] == labels_dict['i_label']]['Prior month'].values[0],
        'a_yc': total[total['Count'] == labels_dict['a_label']]['Prior year'].values[0],
        'i_yc': total[total['Count'] == labels_dict['i_label']]['Prior year'].values[0],
        'a_rac': total[total['Count'] == labels_dict['a_label']]['Rolling average'].values[0],
        'i_rac': total[total['Count'] == labels_dict['i_label']]['Rolling average'].values[0],
        'a_eolyc': total[total['Count'] == labels_dict['a_label']]['Prior year end'].values[0],
        'i_eolyc': total[total['Count'] == labels_dict['i_label']]['Prior year end'].values[0],
        'pa_mc': priority[priority['Count'] == labels_dict['a_label']]['Prior month'].values[0],
        'pi_mc': priority[priority['Count'] == labels_dict['i_label']]['Prior month'].values[0],
        'pa_yc': priority[priority['Count'] == labels_dict['a_label']]['Prior year'].values[0],
        'pi_yc': priority[priority['Count'] == labels_dict['i_label']]['Prior year'].values[0],
        'pa_rac': priority[priority['Count'] == labels_dict['a_label']]['Rolling average'].values[0],
        'pi_rac': priority[priority['Count'] == labels_dict['i_label']]['Rolling average'].values[0],
        'pa_eolyc': priority[priority['Count'] == labels_dict['a_label']]['Prior year end'].values[0],
        'pi_eolyc': priority[priority['Count'] == labels_dict['i_label']]['Prior year end'].values[0],
        }

    colors_dict = {}
    for key, value in variables_dict.items():
        value = float(value)
        if value < 0:
            colors_dict[key] = '008000'
        elif value > 0:
            colors_dict[key] = 'DC143C'
        else:
            colors_dict[key] = '000000'

    variables_pc_dict = {
        'a_mc': total[total['Count'] == labels_dict['a_label']]['Prior month %'].values[0],
        'i_mc': total[total['Count'] == labels_dict['i_label']]['Prior month %'].values[0],
        'a_yc': total[total['Count'] == labels_dict['a_label']]['Prior year %'].values[0],
        'i_yc': total[total['Count'] == labels_dict['i_label']]['Prior year %'].values[0],
        'a_rac': total[total['Count'] == labels_dict['a_label']]['Rolling average %'].values[0],
        'i_rac': total[total['Count'] == labels_dict['i_label']]['Rolling average %'].values[0],
        'a_eolyc': total[total['Count'] == labels_dict['a_label']]['Prior year end %'].values[0],
        'i_eolyc': total[total['Count'] == labels_dict['i_label']]['Prior year end %'].values[0],
        'pa_mc': priority[priority['Count'] == labels_dict['a_label']]['Prior month %'].values[0],
        'pi_mc': priority[priority['Count'] == labels_dict['i_label']]['Prior month %'].values[0],
        'pa_yc': priority[priority['Count'] == labels_dict['a_label']]['Prior year %'].values[0],
        'pi_yc': priority[priority['Count'] == labels_dict['i_label']]['Prior year %'].values[0],
        'pa_rac': priority[priority['Count'] == labels_dict['a_label']]['Rolling average %'].values[0],
        'pi_rac': priority[priority['Count'] == labels_dict['i_label']]['Rolling average %'].values[0],
        'pa_eolyc': priority[priority['Count'] == labels_dict['a_label']]['Prior year end %'].values[0],
        'pi_eolyc': priority[priority['Count'] == labels_dict['i_label']]['Prior year end %'].values[0],
    }
    
    print_dict = {}
    for key, value in variables_pc_dict.items():
        print_dict[key] = str(value) + '% (' + str(variables_dict[key]) + ')'

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    if paragraph.text in labels_dict.keys():
                        paragraph.text = labels_dict[paragraph.text]    
                    if paragraph.text in colors_dict.keys():
                        color = paragraph.text
                        paragraph.text = print_dict[paragraph.text]
                        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor.from_string(colors_dict[color])
                
        table.style.font.name = 'Tahoma'
        table.style.font.size = Pt(12)
    for paragraph in document.paragraphs:
        if 'notes' in paragraph.text:
            notes = total['Notes'].str.cat(sep='\n')
            paragraph.text = notes
            paragraph.style.font.name = 'Tahoma'
            paragraph.style.font.size = Pt(10)

    document.save(f'assets/Waitlist_{date}.docx')
    print(f'assets/Waitlist_{date}.docx' + ' saved')
    return


total, priority, R1C1, date = notes_titles(Waitlist_latest_report_full)
report_update(total, priority, R1C1, date)