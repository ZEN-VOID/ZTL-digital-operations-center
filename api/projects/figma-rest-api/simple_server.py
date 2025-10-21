"""
简单的HTTP服务器 - 用于调试
绕过FastAPI直接提供基本的API功能
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import asyncio
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from app.core.schemas.figma import BatchReplaceRequest, ImageReplaceItem
from app.core.services.batch_replace_service import BatchReplaceService
from app.core.config import get_settings
from app.core.database import get_db_session, init_database


class SimpleAPIHandler(BaseHTTPRequestHandler):
    """简单的API处理器"""

    def do_GET(self):
        """处理GET请求"""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'service': 'figma-rest-api-simple',
                'version': '1.0.0'
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        """处理POST请求"""
        if self.path == '/api/v1/batch-replace/':
            try:
                # 读取请求体
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                request_data = json.loads(post_data.decode())

                # 执行批量替换
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(self._execute_batch_replace(request_data))
                loop.close()

                # 返回结果
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = {'error': str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    async def _execute_batch_replace(self, request_data):
        """执行批量替换任务"""
        await init_database()

        settings = get_settings()
        async for db in get_db_session():
            service = BatchReplaceService(db, settings)

            # 创建请求对象
            replacements = [
                ImageReplaceItem(**item) for item in request_data['replacements']
            ]

            request = BatchReplaceRequest(
                file_key=request_data['file_key'],
                replacements=replacements,
                batch_name=request_data.get('batch_name', 'Batch Replace'),
                auto_export=request_data.get('auto_export', True),
                export_format=request_data.get('export_format', 'png'),
                export_scale=request_data.get('export_scale', 1.0),
                save_to_cos=request_data.get('save_to_cos', False),
                cos_bucket=request_data.get('cos_bucket'),
                cos_directory=request_data.get('cos_directory'),
                cos_region=request_data.get('cos_region')
            )

            # 创建并执行任务
            task = await service.create_batch_replace_task(request)
            await service.execute_batch_replace(task.task_id)

            # 获取最终状态
            final_task = await service.get_task_status(task.task_id)

            return {
                'task_id': final_task.task_id,
                'status': str(final_task.status),
                'total_items': final_task.total_items,
                'completed_items': final_task.completed_items,
                'export_urls': final_task.export_urls or [],
                'error_message': final_task.error_message
            }

    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(port=8003):
    """运行服务器"""
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, SimpleAPIHandler)
    print(f'✅ Simple API Server running on http://127.0.0.1:{port}/')
    print(f'   Health Check: http://127.0.0.1:{port}/health')
    print(f'   Batch Replace: POST http://127.0.0.1:{port}/api/v1/batch-replace/')
    print(f'   Press Ctrl+C to stop')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()