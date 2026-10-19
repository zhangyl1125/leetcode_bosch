from openai import OpenAI
import json

client = OpenAI()

#1.定义工具Tool：
def get_weather(city: str):
    # Demo：真实项目这里调用天气 API
    return {"city": city, "weather": "sunny", "temperature": 25}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["city"],
                "additionalProperties": False
            }
        }
    }
]

TOOL_MAP = {
    "get_weather": get_weather
}


#2.定义 Agent Loop
def agent(user_input: str):
    history = [
        {
            "role": "system",
            "content": "你是一个 ReAct Agent。需要工具时调用工具，否则直接回答。"
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    MAX_STEPS = 5

    for step in range(MAX_STEPS):

        # Think + Action
        response = client.chat.completions.create(
            model="gpt-5.6",
            messages=history,
            tools=TOOLS
        )

        msg = response.choices[0].message
        history.append(msg)

        # 没有 Action -> Final Answer
        if not msg.tool_calls:
            return msg.content

        # Action -> Observation
        for call in msg.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments)

            if name not in TOOL_MAP:
                result = {"error": f"Unknown tool: {name}"}
            else:
                try:
                    result = TOOL_MAP[name](**args)
                except Exception as e:
                    result = {"error": str(e)}

            history.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(
                    result,
                    ensure_ascii=False
                )
            })

    return "Agent 达到最大执行步数，已停止。"


print(agent("帮我查一下上海天气"))