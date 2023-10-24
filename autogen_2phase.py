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
   system_message='''A human admin. ''',
   code_execution_config={"last_n_messages": 3, "use_docker": False },
   max_consecutive_auto_reply=1,
   human_input_mode="TERMINATE",
)
project_manager = autogen.AssistantAgent(
    name="project_manager", 
    system_message=template_role_pm,
    llm_config=llm_config,
)
architect = autogen.AssistantAgent(
    name="architect",
    system_message=template_role_architect,
    llm_config=llm_config,
)


reviewer = autogen.AssistantAgent(
    name="reviewer",
    system_message=template_role_reviewer,
    llm_config=llm_config,
)

groupchat_design = autogen.GroupChat(
    agents=[user_proxy, project_manager, architect, reviewer], messages=[], max_round=20)
groupchat_manager = autogen.GroupChatManager(groupchat=groupchat_design, llm_config=llm_config)

user_proxy.initiate_chat(groupchat_manager, message=query2)

output = user_proxy.last_message()["content"]
