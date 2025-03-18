from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

"""
step1:定义generate_script函数，通过调用函数，得到视频标题和脚本内容
获得视频标题，调用维基百科api获得相关信息，视频脚本内容
"""
def generate_script(subject,video_length,creativity,api_key):
    """
    step2:定义从AI获得标题的提示模板title_template
    从langchain.prompts导入ChatPromptTemplate类；
    通过.from_messages()方法传入消息列表，接收消息列表作为参数
    """
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human","请为{subject}主题想一个吸引人的标题")
        ]
    )


    """
    step3:定义从AI获得脚本内容的提示词模版script_template
    通过.from_messages()方法传入消息列表，接收消息列表作为参数
    """
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human","""你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{wikipedia_search}```""")

        ]
    )

    """
    step4:定义模型model,传入用户所提供的API秘钥
    """
    model = ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_key=api_key,
        base_url = "https://api.aigc369.com/v1",
        temperature=creativity
    )

    """
    step5:组装获得视频标题和脚本的链 
    """

    title_chain = title_template | model
    script_chain = script_template | model

    """
    step6:获得AI返回标题消息实例title
    调用.invoke，通过invoke返回视频标题消息，通过返回消息的.content属性
    获得AI返回的视频标题内容title
    """
    title = title_chain.invoke(
        {
            "subject":subject
        }
    ).content
    """
    step7:获得维基百科返回消息实例search
    从langchain_community.utilities模块中导入WikipediaA；
    通过PIWrapperl类（能够通过维基百科官方API进行搜索，并返回搜
    索结果摘要）获得维基百科返回消息内容search
    """
    search = WikipediaAPIWrapper(lang="zh")
    search_result = search.run(subject)

    """
    step8:获得AI返回脚本内容消息实例
    调用.invoke，通过invoke返回视频脚本消息，通过返回消息的.content属性
    获得AI返回的视频脚本内容script
    """
    script = script_chain.invoke(
        {
            "title":title,"duration":video_length,"wikipedia_search":search_result
            # "title": title, "duration": video_length,
        }
    ).content

    return search_result,title,script
"""
step9:调用generate_script()函数
"""
#print(generate_script("sora模型",1,0.7,""))
