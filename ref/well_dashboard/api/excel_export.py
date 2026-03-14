"""
Async Excel Export Module for Well Dashboard API
"""

import pandas as pd
import xlsxwriter
from datetime import datetime
from typing import Dict, List
import os
import aiofiles
from api.config import settings


async def ensure_export_dir():
    """Ensure export directory exists"""
    os.makedirs(settings.EXPORT_PATH, exist_ok=True)


async def export_well_to_excel(well_data: Dict, filename: str = None) -> str:
    """Export well data to Excel with multiple sheets"""
    await ensure_export_dir()
    
    if not filename:
        well_name = well_data['well_name'].replace(' ', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{well_name}_{timestamp}.xlsx"
    
    filepath = os.path.join(settings.EXPORT_PATH, filename)
    
    # Use pandas ExcelWriter with xlsxwriter engine
    with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#1f4e79',
            'font_color': 'white',
            'border': 1
        })
        
        # Sheet 1: Header
        header_info = [
            ['Field', 'Value'],
            ['Well Name', well_data.get('well_name', '')],
            ['Well Number', well_data.get('well_number', '')],
            ['API Number', well_data.get('api_number', '')],
            ['Well Type', well_data.get('well_type', '')],
            ['Current Status', well_data.get('current_status', '')],
            ['Surface Latitude', well_data.get('surface_lat', '')],
            ['Surface Longitude', well_data.get('surface_lon', '')],
            ['Bottom Hole Latitude', well_data.get('bottom_hole_lat', '')],
            ['Bottom Hole Longitude', well_data.get('bottom_hole_lon', '')],
            ['Spud Date', well_data.get('spud_date', '')],
            ['Completion Date', well_data.get('completion_date', '')],
            ['Release Date', well_data.get('release_date', '')],
            ['Total Depth (Planned)', well_data.get('total_depth_planned', '')],
            ['Total Depth (Actual)', well_data.get('total_depth_actual', '')],
            ['Measured Depth (Planned)', well_data.get('measured_depth_planned', '')],
            ['Measured Depth (Actual)', well_data.get('measured_depth_actual', '')],
            ['TVD (Planned)', well_data.get('true_vertical_depth_planned', '')],
            ['TVD (Actual)', well_data.get('true_vertical_depth_actual', '')],
            ['Kick Off Point', well_data.get('kick_off_point', '')],
            ['Rig Name', well_data.get('rig_name', '')],
            ['Contractor', well_data.get('contractor', '')],
            ['Description', well_data.get('description', '')],
            ['Created At', well_data.get('created_at', '')],
            ['Updated At', well_data.get('updated_at', '')]
        ]
        
        header_df = pd.DataFrame(header_info[1:], columns=header_info[0])
        header_df.to_excel(writer, sheet_name='Well Header', index=False)
        worksheet = writer.sheets['Well Header']
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 40)
        
        # Sheet 2: Status History
        if well_data.get('status_history'):
            status_df = pd.DataFrame(well_data['status_history'])
            if not status_df.empty:
                status_df = status_df[['changed_at', 'old_status', 'new_status', 'changed_by_username', 'notes']]
                status_df.columns = ['Date', 'Old Status', 'New Status', 'Changed By', 'Notes']
                status_df.to_excel(writer, sheet_name='Status History', index=False)
                worksheet = writer.sheets['Status History']
                worksheet.set_column('A:A', 20)
                worksheet.set_column('B:C', 15)
                worksheet.set_column('D:D', 15)
                worksheet.set_column('E:E', 40)
        
        # Sheet 3: Wellbore Plan
        if well_data.get('wellbore_plan'):
            wb_plan_df = pd.DataFrame(well_data['wellbore_plan'])
            if not wb_plan_df.empty:
                wb_plan_df = wb_plan_df[['section_name', 'section_type', 'top_md', 'bottom_md', 
                                          'top_tvd', 'bottom_tvd', 'hole_size', 'hole_size_unit',
                                          'mud_weight', 'mud_type', 'description']]
                wb_plan_df.columns = ['Section', 'Type', 'Top MD', 'Bottom MD', 
                                     'Top TVD', 'Bottom TVD', 'Hole Size', 'Unit',
                                     'Mud Weight', 'Mud Type', 'Description']
                wb_plan_df.to_excel(writer, sheet_name='Wellbore Plan', index=False)
        
        # Sheet 4: Wellbore Actual
        if well_data.get('wellbore_actual'):
            wb_actual_df = pd.DataFrame(well_data['wellbore_actual'])
            if not wb_actual_df.empty:
                wb_actual_df = wb_actual_df[['section_name', 'section_type', 'top_md', 'bottom_md',
                                             'top_tvd', 'bottom_tvd', 'hole_size', 'hole_size_unit',
                                             'mud_weight', 'mud_type', 'description']]
                wb_actual_df.columns = ['Section', 'Type', 'Top MD', 'Bottom MD',
                                       'Top TVD', 'Bottom TVD', 'Hole Size', 'Unit',
                                       'Mud Weight', 'Mud Type', 'Description']
                wb_actual_df.to_excel(writer, sheet_name='Wellbore Actual', index=False)
        
        # Sheet 5: Casing Plan
        if well_data.get('casing_plan'):
            casing_plan_df = pd.DataFrame(well_data['casing_plan'])
            if not casing_plan_df.empty:
                casing_plan_df = casing_plan_df[['string_name', 'string_type', 'top_md', 'bottom_md',
                                                 'top_tvd', 'bottom_tvd', 'casing_od', 'casing_id',
                                                 'weight', 'grade', 'connection', 'cement_top_md',
                                                 'cement_bottom_md', 'cement_volume', 'description']]
                casing_plan_df.columns = ['String Name', 'Type', 'Top MD', 'Bottom MD',
                                         'Top TVD', 'Bottom TVD', 'OD (in)', 'ID (in)',
                                         'Weight (lb/ft)', 'Grade', 'Connection', 'Cement Top MD',
                                         'Cement Bottom MD', 'Cement Volume', 'Description']
                casing_plan_df.to_excel(writer, sheet_name='Casing Plan', index=False)
        
        # Sheet 6: Casing Actual
        if well_data.get('casing_actual'):
            casing_actual_df = pd.DataFrame(well_data['casing_actual'])
            if not casing_actual_df.empty:
                casing_actual_df = casing_actual_df[['string_name', 'string_type', 'top_md', 'bottom_md',
                                                     'top_tvd', 'bottom_tvd', 'casing_od', 'casing_id',
                                                     'weight', 'grade', 'connection', 'installed_date',
                                                     'cement_top_md', 'cement_bottom_md', 'cement_volume', 'description']]
                casing_actual_df.columns = ['String Name', 'Type', 'Top MD', 'Bottom MD',
                                           'Top TVD', 'Bottom TVD', 'OD (in)', 'ID (in)',
                                           'Weight (lb/ft)', 'Grade', 'Connection', 'Installed Date',
                                           'Cement Top MD', 'Cement Bottom MD', 'Cement Volume', 'Description']
                casing_actual_df.to_excel(writer, sheet_name='Casing Actual', index=False)
        
        # Sheet 7: Tubular Plan
        if well_data.get('tubular_plan'):
            tubular_plan_df = pd.DataFrame(well_data['tubular_plan'])
            if not tubular_plan_df.empty:
                tubular_plan_df = tubular_plan_df[['string_name', 'string_type', 'component_name',
                                                   'top_md', 'bottom_md', 'outer_diameter', 'inner_diameter',
                                                   'weight', 'length', 'grade', 'connection', 'material', 'description']]
                tubular_plan_df.columns = ['String Name', 'Type', 'Component', 'Top MD', 'Bottom MD',
                                          'OD (in)', 'ID (in)', 'Weight (lb/ft)', 'Length (ft)',
                                          'Grade', 'Connection', 'Material', 'Description']
                tubular_plan_df.to_excel(writer, sheet_name='Tubular Plan', index=False)
        
        # Sheet 8: Tubular Actual
        if well_data.get('tubular_actual'):
            tubular_actual_df = pd.DataFrame(well_data['tubular_actual'])
            if not tubular_actual_df.empty:
                tubular_actual_df = tubular_actual_df[['string_name', 'string_type', 'component_name',
                                                       'top_md', 'bottom_md', 'outer_diameter', 'inner_diameter',
                                                       'weight', 'length', 'grade', 'connection', 'material', 'description']]
                tubular_actual_df.columns = ['String Name', 'Type', 'Component', 'Top MD', 'Bottom MD',
                                            'OD (in)', 'ID (in)', 'Weight (lb/ft)', 'Length (ft)',
                                            'Grade', 'Connection', 'Material', 'Description']
                tubular_actual_df.to_excel(writer, sheet_name='Tubular Actual', index=False)
        
        # Sheet 9: Survey Plan
        if well_data.get('survey_plan'):
            survey_plan_df = pd.DataFrame(well_data['survey_plan'])
            if not survey_plan_df.empty:
                survey_plan_df = survey_plan_df[['md', 'inclination', 'azimuth', 'tvd',
                                                 'northing', 'easting', 'vertical_section', 'dls',
                                                 'tool_face', 'section', 'survey_company', 'tool_type']]
                survey_plan_df.columns = ['MD (ft)', 'Inc (°)', 'Azm (°)', 'TVD (ft)',
                                         'Northing', 'Easting', 'VS (ft)', 'DLS (°/100ft)',
                                         'Tool Face', 'Section', 'Survey Company', 'Tool Type']
                survey_plan_df.to_excel(writer, sheet_name='Survey Plan', index=False)
        
        # Sheet 10: Survey Actual
        if well_data.get('survey_actual'):
            survey_actual_df = pd.DataFrame(well_data['survey_actual'])
            if not survey_actual_df.empty:
                survey_actual_df = survey_actual_df[['md', 'inclination', 'azimuth', 'tvd',
                                                     'northing', 'easting', 'vertical_section', 'dls',
                                                     'tool_face', 'section', 'survey_date', 'survey_company', 'tool_type']]
                survey_actual_df.columns = ['MD (ft)', 'Inc (°)', 'Azm (°)', 'TVD (ft)',
                                           'Northing', 'Easting', 'VS (ft)', 'DLS (°/100ft)',
                                           'Tool Face', 'Section', 'Survey Date', 'Survey Company', 'Tool Type']
                survey_actual_df.to_excel(writer, sheet_name='Survey Actual', index=False)
    
    return filepath


async def export_project_to_excel(project_data: Dict, filename: str = None) -> str:
    """Export entire project to Excel"""
    await ensure_export_dir()
    
    project = project_data['project']
    wells = project_data['wells']
    
    if not filename:
        project_name = project['project_name'].replace(' ', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{project_name}_Project_{timestamp}.xlsx"
    
    filepath = os.path.join(settings.EXPORT_PATH, filename)
    
    with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#1f4e79',
            'font_color': 'white',
            'border': 1
        })
        
        # Sheet 1: Project Summary
        summary_data = [
            ['Project Name', project['project_name']],
            ['Project Type', project['project_type'].replace('_', ' ').title()],
            ['Pad Name', project.get('pad_name', 'N/A')],
            ['Surface Location', f"{project.get('surface_location_lat', 'N/A')}, {project.get('surface_location_lon', 'N/A')}"],
            ['Field', project.get('field', 'N/A')],
            ['Operator', project.get('operator', 'N/A')],
            ['Description', project.get('description', 'N/A')],
            ['Number of Wells', len(wells)],
            ['Created At', project.get('created_at', 'N/A')]
        ]
        
        summary_df = pd.DataFrame(summary_data, columns=['Field', 'Value'])
        summary_df.to_excel(writer, sheet_name='Project Summary', index=False)
        worksheet = writer.sheets['Project Summary']
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 50)
        
        # Sheet 2: Wells Summary
        if wells:
            wells_summary = []
            for well_data in wells:
                well = well_data
                wells_summary.append({
                    'Well Name': well.get('well_name', ''),
                    'Well Number': well.get('well_number', ''),
                    'API Number': well.get('api_number', ''),
                    'Status': well.get('current_status', ''),
                    'Type': well.get('well_type', ''),
                    'Spud Date': well.get('spud_date', ''),
                    'Planned MD': well.get('measured_depth_planned', ''),
                    'Actual MD': well.get('measured_depth_actual', ''),
                    'Planned TVD': well.get('true_vertical_depth_planned', ''),
                    'Actual TVD': well.get('true_vertical_depth_actual', '')
                })
            
            wells_df = pd.DataFrame(wells_summary)
            wells_df.to_excel(writer, sheet_name='Wells Summary', index=False)
            worksheet = writer.sheets['Wells Summary']
            for i, col in enumerate(wells_df.columns):
                worksheet.write(0, i, col, header_format)
        
        # Individual well sheets
        for well_data in wells:
            well = well_data
            sheet_name = well['well_name'][:31]  # Excel sheet name max 31 chars
            
            well_summary = [
                ['Well Name', well.get('well_name', '')],
                ['Well Number', well.get('well_number', '')],
                ['API Number', well.get('api_number', '')],
                ['Status', well.get('current_status', '')],
                ['Type', well.get('well_type', '')],
                ['Spud Date', well.get('spud_date', '')],
                ['Completion Date', well.get('completion_date', '')],
                ['Total Depth (Planned)', well.get('total_depth_planned', '')],
                ['Total Depth (Actual)', well.get('total_depth_actual', '')],
                ['MD (Planned)', well.get('measured_depth_planned', '')],
                ['MD (Actual)', well.get('measured_depth_actual', '')],
                ['TVD (Planned)', well.get('true_vertical_depth_planned', '')],
                ['TVD (Actual)', well.get('true_vertical_depth_actual', '')],
                ['Rig', well.get('rig_name', '')],
                ['Contractor', well.get('contractor', '')]
            ]
            
            well_df = pd.DataFrame(well_summary, columns=['Field', 'Value'])
            well_df.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]
            worksheet.set_column('A:A', 25)
            worksheet.set_column('B:B', 40)
    
    return filepath


async def get_export_files() -> List[Dict]:
    """Get list of exported files"""
    await ensure_export_dir()
    files = []
    
    for filename in os.listdir(settings.EXPORT_PATH):
        if filename.endswith('.xlsx'):
            filepath = os.path.join(settings.EXPORT_PATH, filename)
            stat = os.stat(filepath)
            files.append({
                'filename': filename,
                'filepath': filepath,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })
    
    return sorted(files, key=lambda x: x['created'], reverse=True)


async def delete_export_file(filename: str) -> bool:
    """Delete an export file"""
    filepath = os.path.join(settings.EXPORT_PATH, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False
