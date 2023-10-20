import autogen
from autogen import config_list_from_json
from templates import role_architect, role_pm, role_reviewer

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

llm_config = {
    "config_list": config_list,
    "request_timeout": 120,
    "seed": 42 #possible can be removed
}

query2 = "I want to create a new facebook like app"

user_proxy = autogen.UserProxyAgent(
   name="User_proxy",
   is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
   system_message='''A human admin. Your task, once the agreement has been reached, is to output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like format example,\
    and only output the json inside this tag, nothing else\
    \
    FORMAT_EXAMPLE: \
    [CONTENT]\
    {\
        "Original Requirements": "",\
        "Product Goals": [],\
        "User Stories": [],\
        "Requirement Analysis": "",\
        "UI Design draft": "",\
        "Architecture Plan": "",\
        "Technical Stack Recommendations": "",\
        "Infrastructure Needs": "",\
        "Integration Points": [],\
        "Potential Challenges": "",\
        "Operational Steps": "",\
        "Anything UNCLEAR": "",\
    }\
    [/CONTENT]\
    \
    Reply TERMINATE when the task is done.''',
   code_execution_config={"last_n_messages": 3, "use_docker": False },
   max_consecutive_auto_reply=4,
   human_input_mode="TERMINATE",
)
project_manager = autogen.AssistantAgent(
    name="project_manager", 
    system_message=role_pm,
    llm_config=llm_config,
)
architect = autogen.AssistantAgent(
    name="architect",
    system_message=role_architect,
    llm_config=llm_config,
)

reviewer = autogen.AssistantAgent(
    name="reviewer",
    system_message=role_reviewer,
    llm_config=llm_config,
)

groupchat_design = autogen.GroupChat(
    agents=[user_proxy, project_manager, architect, reviewer], messages=[], max_round=20)
groupchat_manager = autogen.GroupChatManager(groupchat=groupchat_design, llm_config=llm_config)

user_proxy.initiate_chat(groupchat_manager, message=query2)

output = user_proxy.last_message()["content"]