import random

def get_prompt(post="", min_num_tasks=10):

#     num_tasks = min(len(TASKS_LIST), min_num_tasks)

#     numbers = list(range(len(TASKS_LIST)))
#     random_numbers = random.sample(range(len(TASKS_LIST)), num_tasks)
    
#     tasks = [TASKS_LIST[i] for i in random_numbers]
    
#     total_tasks = PRIOR_TASKS + tasks

    # THUC ver_GPT4
    sys_prompt_template = '''
### Article ###

{post}

### Instruction ###
Dựa trên nội dung của bài viết được cung cấp, hãy thực hiện hai yêu cầu sau:

1. Tạo ra một danh sách gồm 5 câu hỏi khó mà không thể tìm thấy câu trả lời trong bài viết. Những câu hỏi này phải liên quan đến chủ đề của bài viết nhưng không được trực tiếp trả lời bởi nội dung bài viết.

2. Tạo ra 5 cặp hỏi-đáp, trong đó mỗi cặp bao gồm một câu hỏi và câu trả lời tương ứng. Các câu hỏi này cần có thông tin có thể suy luận từ bài viết, yêu cầu sự kết nối và suy luận phức tạp thông tin để trả lời..

Yêu cầu bắt buộc: Chỉ trả về dưới dạng JSON như sau:
{{
  "Danh sách câu hỏi không có câu trả lời": [ "Câu hỏi 1 không có trong bài viết là gì?", "Câu hỏi 2 không có trong bài viết là gì?", ... ],
  "Danh sách cặp hỏi-đáp có câu trả lời": [ 
  {{"Câu hỏi": "Câu hỏi khó cần suy luận từ bài viết?", 
    "Câu trả lời": "Câu trả lời cho câu hỏi dựa trên suy luận từ bài viết."}}, 
  ...
  ]
}}
'''

    return sys_prompt_template.format(post=post)    


# -------------------------------------------------------------------------------------

# TASKS_LIST = [
# "3. Sinh ra tiêu đề",
# "4. Tạo tên chủ đề",
# "5. Tạo 5 bình luận có thể có",
# "6. Phân loại nội dung", 
# "7. Phát hiện các thực thể",
# "8. Trích xuất thông tin với các thuộc tính có thể có trong bài",
# "9. Tìm sản phẩm có thể liên quan",
# "10. Tạo đánh giá",
# "11. Tạo 2 câu hỏi và câu trả lời tương ứng",
# "12. Sinh ra bình luận ý định mua hàng",
# "13. Phân loại thực thể",
# "14. Dự đoán nhóm khách hàng tiềm năng",
# "15. Phát hiện giá trị thuộc tính",
# "16. Trích xuất thông tin người mua hoặc bán",
# "17. Sinh ra bài viết tương tự với sắc thái khác", 
# "18. Sinh ra thuộc tính có thể trích xuất phù hợp",
# "19. Sửa lỗi chính tả và viết tắt",
# "20. Phân tích các emoji",
# "21. Phân tích thái độ cảm xúc",
# "22. Sinh ra nội dung với sắc thái cảm xúc khác",
# "23. Sinh ra ý tưởng quảng cáo sản phẩm",
# "24. Sinh ra câu hỏi thăm dò ý kiến khách hàng",
# "25. Sinh 1 FAQ cho sản phẩm",
# "26. Tạo 5 bình luận có thể có sắc thái cảm xúc khác",
# "27. Tạo 5 hashtag cho bài viết"]

# PRIOR_TASKS = ["1. Phân tích và tóm tắt nội dung", 
#                "2. Trích xuất thông tin với các thuộc tính có thể có trong bài"]


#     sys_prompt_template = """Bạn là chuyên gia social listening phân tích toàn diện và đầy đủ cho bài đăng
# Các tác vụ gợi ý như sau: câu chủ đề, tóm tắt ngắn gọn ý chính, đánh giá tổng quan thái độ, trích xuất thông tin, liện hệ trực tiếp, liên hệ trực tuyến, trích xuất thực thể và các thuộc tính, trích xuất cảm xúc theo khía cạnh, phân tích ý nghĩa ẩn dụ các emoji, các highlight keywords.
# Lưu ý:  chỉ trả về json. cuối json phân tích cần đưa ra vài quan điểm trái chiều với bài và lời khuyên đối với người đọc. 
# Bài Viết:
# {post}
# """ # KHANG
#     return total_tasks, sys_prompt_template.format(post=post)    
# -------------------------------------------------------------------------------------

#     sys_prompt_template = """[no closing notes] Bạn là một chuyên gia social listening. Khi nhận một bài viết, hãy ngẫu nhiên chọn một số ít tác vụ từ danh sách dưới đây để thực hiện. Không cần thực hiện tất cả các tác vụ, chỉ cần đảm bảo rằng mỗi tác vụ được chọn thực hiện một cách toàn diện, chính xác và trung thực, tránh cung cấp thông tin sai lệch không có trong bài viết. Các phản hồi nên sử dụng định dạng xen kẽ giữa JSON và văn bản. Không cần thêm bất kỳ câu mở đầu hoặc kết thúc nào khác ngoài thông tin cần thiết cho từng tác vụ. Danh sách các tác vụ có thể chọn bao gồm:

# {tasks}

# Hãy lựa chọn chỉ một số ít các tác vụ để thực hiện và xem xét lại các phản hồi, đảm bảo sử dụng cả hai định dạng JSON và văn bản. Bài viết cần phân tích là: 

# {post}
# """ # BAO
#     return total_tasks, sys_prompt_template.format(tasks=str(total_tasks), post=post)    
# -------------------------------------------------------------------------------------

 
#     #THUC ver1
#     sys_prompt_template = """Bài viết vài bình luận trên mạng xã hội tương ứng như sau, hãy đọc và thực hiện nhiệm vụ bên dưới: 
# {post}
# Nhiệm vụ: 
# Hãy thực hiện các phân tích social listening sau: 
# Cho bài viết: phân tích nội dung chính, trích xuất thực thể chủ đề của bài viết, tình cảm của bài viết ?  giải thích emoji bài viết.

# Cho bình luận: giải thích dài, rõ nghĩa nội dụng bình luận kèm phân loại tích cực/tiêu cực/trung tính cho từng bình luận và đề xuất các emoji cho từng bình luận kèm ý nghĩa, trích xuất đơn hàng thành dạng json {{mặt hàng, số lượng,  giá tiền, thuộc tính khác..., sdt}}, cuối cùng hãy tạo nhận xét quan điểm chung của các bình luận về bài viết. Lưu ý: Chỉ trả về json."""

#     return sys_prompt_template.format(post=post)   
# -------------------------------------------------------------------------------------

#     # THUC ver2
#     sys_prompt_template = """Bài viết vài bình luận trên mạng xã hội tương ứng như sau, hãy đọc và thực hiện nhiệm vụ bên dưới: 
# {post}
# Nhiệm vụ: 
# Hãy thực hiện tác phân tích social listening sau: 
# Đối với bài viết: cho biết nội dung chính của bài viết.
# Đối với bình luận: hãy chỉ ra ý đồ của từng bình luận, hãy tạo câu trả lời cho từng bình luận kèm emoji phù hợp dựa vào ngữ cảnh bài viết
# Lưu ý trả về JSON."""

#     return sys_prompt_template.format(post=post)   

# -------------------------------------------------------------------------------------

#     # THUC ver3
#     sys_prompt_template = """Cung cấp các bình luận trên mạng xã hội tương ứng như sau, Bạn là một Trợ lý AI hãy đọc và thực hiện nhiệm vụ bên dưới: 

# Danh sách các bình luận: 
# {post}

# Nhiệm vụ: 
# Hãy phân tích tổng hợp cảm xúc của đa số về từng khía cạnh của sản phẩm được nhắc đến"""

#     return sys_prompt_template.format(post=post)    
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------

#     # THUC ver4

# end = ['được đề cập đến trong sản phẩm', 'là điểm nổi bật của sản phẩm', 'sản phẩm được đánh giá trong bài']
# start = [
#     'Tiếp cận từng phần một cách đầy đủ và sau đó tổng hợp ý kiến của đa số về các khía cạnh',
#     'Cho biết từng khía cạnh một và sau đó tập trung tổng hợp ý kiến chung từ đa số về khía cạnh',
#     'Phân tích chi tiết từng khía cạnh và sau đó tổng hợp quan điểm phổ biến của đa số, tạo nên cái nhìn toàn diện các quan điểm']

#     sys_prompt_template = """Cung cấp các bình luận trên mạng xã hội tương ứng như sau, Bạn là một Trợ lý AI hãy đọc và thực hiện nhiệm vụ bên dưới: 

# Danh sách các bình luận: 
# {post}

# Nhiệm vụ: 
# random choice"""

#     return sys_prompt_template.format(post=post)    
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------

#     # THUC ver5

# instructs =  [
#     'Tóm tắt một cách ngắn gọn cảm nhận phổ biến của đa số về các khía cạnh của sản phẩm',
#     'Phân tích ngắn gọn nhưng toàn diện về cảm xúc của số đông đối với các quan điểm từ các đánh giá về sản phẩm',
#     'Tổng hợp ngắn gọn cảm xúc của hầu hết bình luận đánh giá về sản phẩm',
#     'Tóm lược ngắn nhưng đầy đủ về cảm nhận đám đông từ các đánh giá đối với các quan điểm về sản phẩm']
#     sys_prompt_template = """Cung cấp các bình luận trên mạng xã hội tương ứng như sau, Bạn là một Trợ lý AI hãy đọc và thực hiện nhiệm vụ bên dưới: 

# Danh sách các bình luận: 
# {post}

# Nhiệm vụ: 
# random choice"""

#     return sys_prompt_template.format(post=post)    
# -------------------------------------------------------------------------------------

# LIST_TASK = ['Phân loại danh mục ngành hàng và tên sản phẩm (nếu có) từ bài viết', 
#              'Tạo ra một bản tóm tắt mới dựa vào nội dung bài viết',
#              'Phân tích ý đồ của từng bình luận',
#              'Phân tích thông tin thực thể chi tiết và PHẢI trả về dưới dạng JSON chuyên nghiệp.',
#              'Bài viết hướng đến nhóm đối tượng người dùng nào?', 
#              'Phân loại cảm xúc của các bình luận',
#              'Đề xuất các emoji phù hợp và giải thích',
#              'Phân tích thông tin phong cách của bài viết: ngôn ngữ, cấu trúc câu, và thậm chí là phong cách viết để có cái nhìn về tính cách.'
#             ]

#     # THUC ver6
#     task = random.sample(LIST_TASK, k=len(LIST_TASK))
#     sys_prompt_template = '''Tạo 1 đoạn đối thoại tự nhiên giữa kỹ sư AI và Trợ lý AI xử lý ngôn ngữ tự nhiên. Nội dung đoạn đối thoại xung quanh nội dung bài viết và bình luận được cung cấp. Đối với kỹ sư AI sẽ lựa chọn ít nhất 5 tác vụ dựa trên danh sách các tác vụ. Đối với trợ lý AI sẽ thực hiện tác vụ và trả lời kết quả sau khi thực hiện. Các tác vụ NLP gợi ý ngẫu nhiên như sau: {task}.
# {post}
# Lưu ý: Phải trả về đoạn đối thoại dưới dạng JSON như sau:
# [
# {{"kỹ sư AI hỏi": "",
# "kết quả từ trợ lý AI NLP": ""}},
# {{"kỹ sư AI hỏi": "",
# "kết quả từ trợ lý AI NLP": ""}},
# ]'''

#     return sys_prompt_template.format(task=task,post=post)  
