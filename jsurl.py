import re
import html
import os
import webbrowser

def extract_path_from_js(file_path):  
    # 正则表达式，用于查找JavaScript代码中的路径  
    pattern = r'(?:get|post|put|delete)\(["\']([^"\']+)["\']|\/cgi-bin\/playguide\.cgi\?action=\d+&cmd=\d+&key='
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:  
            content = file.read()  
            # 查找所有匹配的路径
            matches = re.findall(pattern, content)
            # 过滤掉空字符串
            matches = [match for match in matches if match]
            return matches
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return []

def write_paths_to_html(paths, output_file):  
    # 创建HTML文件并写入提取的路径  
    with open(output_file, 'w', encoding='utf-8') as file:  
        file.write('<html>\n<head>\n<title>提取的路径</title>\n')  
        
        # CSS样式，增加按钮和敏感路径的样式
        file.write('<style>\n')  
        file.write('table { width: 100%; border-collapse: collapse; }\n')  
        file.write('th, td { border: 1px solid black; padding: 8px; text-align: left; }\n')  
        file.write('th { background-color: #f2f2f2; }\n')
        file.write('button { background-color: #B0E2FF; padding: 8px 16px; border: none; cursor: pointer; }\n')  # 按钮背景颜色
        file.write('.highlight { background-color: #AB82FF; }\n')  # 高亮样式
        file.write('#urlInput{height: 35px;width: 350px;}\n')
        file.write('body { text-align: center; }\n')  # 使内容居中
        file.write('table { margin: 0 auto; }\n')  # 使表格居中
        file.write('td:hover { background-color: #DCE2F1; cursor: pointer; }\n')  # 鼠标悬停样式

        # 样式用于显示复制成功的提示
        file.write('#notification { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: #DCE2F1; padding: 10px; border: 1px solid #B0B0B0; border-radius: 5px; display: none; }\n')
        file.write('</style>\n')  
       
        # JavaScript脚本，处理URL的添加和路径高亮
        file.write('<script>\n')  
        file.write('var originalPaths = [];\n')  # 存储原始路径
        
        file.write('function addUrl() {\n')  
        file.write('    var url = document.getElementById("urlInput").value;\n')  
        
        # 自动匹配并添加http://前缀
        file.write('    if (!/^https?:\\/\\//i.test(url)) {\n')  
        file.write('        url = "http://" + url;\n')  
        file.write('    }\n')  

        # 确保URL以单个斜杠结束
        file.write('    if (!/\\/$/.test(url)) {\n')  
        file.write('        url += "/";\n')  
        file.write('    }\n')  

        # 处理URL中多余的斜杠
        file.write('    url = url.replace(/\\/\\/+$/, "/");\n')  # 处理末尾多余的斜杠
        file.write('    var table = document.getElementById("pathTable");\n')  
        file.write('    // 清除之前的URL\n')  
        file.write('    for (var i = 1; i < table.rows.length; i++) {\n')  
        file.write('        var cell = table.rows[i].cells[1];\n')  # 获取路径的单元格
        file.write('        var originalPath = originalPaths[i - 1];\n')  # 使用存储的原始路径
        file.write('        cell.innerHTML = url + originalPath;\n')  # 添加新的URL
        file.write('    }\n')  
        file.write('}\n')  
        
        # 处理回车键确认
        file.write('function handleKeyPress(event) {\n')  
        file.write('    if (event.key === "Enter") {\n')  
        file.write('        addUrl();\n')  
        file.write('    }\n')  
        file.write('}\n')  
        
        # 复制到剪切板的功能
        file.write('function copyToClipboard(text) {\n')  
        file.write('    var textarea = document.createElement("textarea");\n')  
        file.write('    textarea.value = text;\n')  
        file.write('    document.body.appendChild(textarea);\n')  
        file.write('    textarea.select();\n')  
        file.write('    document.execCommand("copy");\n')  
        file.write('    document.body.removeChild(textarea);\n')  
        file.write('}\n')  
        
        # 显示通知
        file.write('function showNotification(message) {\n')  
        file.write('    var notification = document.getElementById("notification");\n')  
        file.write('    notification.textContent = message;\n')  
        file.write('    notification.style.display = "block";\n')  
        file.write('    setTimeout(function() {\n')  
        file.write('        notification.style.display = "none";\n')  
        file.write('    }, 2000);\n')  # 2秒后隐藏通知
        file.write('}\n')  
        
        file.write('window.onload = function() {\n')  
        file.write('    document.getElementById("urlInput").focus();\n')  # 页面加载时自动聚焦到输入框
        file.write('    var table = document.getElementById("pathTable");\n')  
        file.write('    for (var i = 1; i < table.rows.length; i++) {\n')  
        file.write('        originalPaths.push(table.rows[i].cells[1].innerHTML);\n')  # 存储原始路径
        
        # 检查路径是否包含敏感字符并高亮显示
        file.write('        var path = table.rows[i].cells[1].innerHTML;\n')  
        file.write('        if (path.match(/del|delete|update|create/i)) {\n')  
        file.write('            table.rows[i].classList.add("highlight");\n')  
        file.write('        }\n')  
        
        # 添加点击复制功能
        file.write('        table.rows[i].cells[1].onclick = function() {\n')  
        file.write('            copyToClipboard(this.innerText);\n')  
        file.write('            showNotification("路径已复制到剪切板");\n')  # 显示通知
        file.write('        };\n')  
        file.write('    }\n')  
        file.write('}\n')  
        file.write('</script>\n')  
        
        file.write('</head>\n<body>\n')  
        file.write('<h1>提取的路径</h1>\n')  
        file.write(f'<p>共提取到 {len(paths)} 条数据</p>\n')  
        
        # 输入框和按钮，增加几个空行
        file.write('<input type="text" id="urlInput" placeholder="输入URL" onkeypress="handleKeyPress(event)" />\n')  # 添加回车事件
        file.write('<button onclick="addUrl()">一键加入URL</button>\n')  
        file.write('<br><br><br><br>\n')  # 增加空行
        
        file.write('<div id="notification"></div>\n')  # 通知区域
        
        file.write('<table id="pathTable">\n<tr><th>编号</th><th>路径</th></tr>\n')  # 增加编号列
        
        # 写入路径，自动处理HTML转义，并添加编号
        for idx, path in enumerate(paths, 1):  # 从1开始编号
            escaped_path = html.escape(path)  
            file.write(f'<tr><td>{idx}</td><td>{escaped_path}</td></tr>\n')  
        
        file.write('</table>\n</body>\n</html>')






# 主程序逻辑
js_file_path = 'js.txt'  
output_html_file = 'js路径.html'

# 检查是否存在同名文件
if os.path.exists(output_html_file):
    choice = input(f"{output_html_file} 已存在。是否删除并生成新的文件？ (y/n): ")
    if choice.lower() == 'y':
        os.remove(output_html_file)
        print(f"{output_html_file} 已删除。")

# 提取路径并生成HTML文件
extracted_paths = extract_path_from_js(js_file_path)  
write_paths_to_html(extracted_paths, output_html_file)

# 获取完整路径并打印
full_output_path = os.path.abspath(output_html_file)
print(f'提取的路径已写入到 {full_output_path}')

# 自动打开生成的HTML文件
webbrowser.open(full_output_path)
