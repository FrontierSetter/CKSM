import pyecharts.options as opts
from pyecharts.charts import Line

"""
Gallery 使用 pyecharts 1.1.0
参考地址: https://echarts.baidu.com/examples/editor.html?c=area-stack
目前无法实现的功能:
暂无
"""

curFile = open('uksm_pages_map_cnt.log', 'r')

pre_merged = 0
pre_notmerged = 0
cur_merged = 0
cur_notmerged = 0

x_data = []
truly_merged = []
not_merged = []

while True:
    curLine = curFile.readline()
    if curLine == '':
        break
    x_data.append(curLine)
    curFile.readline()
    cur_merged = int(curFile.readline())
    cur_notmerged = int(curFile.readline())

    truly_merged.append(cur_merged-pre_merged)
    not_merged.append(cur_notmerged-pre_notmerged)

    pre_merged = cur_merged
    pre_notmerged = cur_notmerged


print(len(truly_merged))


(
    Line()
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name="truly_merged",
        stack="总量",
        y_axis=truly_merged,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        series_name="not_merged",
        stack="总量",
        y_axis=not_merged,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="UKSM"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        datazoom_opts=opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),
    )
    .render("UKSM-diff.html")
)