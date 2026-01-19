import uuid
import requests

from colors import print_user_request, print_header, print_agent_respond


def invoke(prompt, user_id, session_id, print_output=True):
    """Make an HTTP POST request and return formatted request/response details"""
    headers = {
        'Content-Type': 'application/json',
        'user_id': user_id,
        'session_id': session_id,
    }
    data = {"prompt": prompt}

    if print_output:
        print_user_request([prompt])

    response = requests.post(
        'http://localhost:8000/invoke',
        headers=headers,
        json=data
    )

    response_text = response.text

    try:
        json_response = response.json()
        if print_output:
            print_agent_respond([json_response])
        return response_text
    except requests.exceptions.JSONDecodeError as e:
        if print_output:
            print(f"JSON Decode Error: {e}")
            print(f"Raw Response Text: {response_text}")
        return response_text


def demo1():
    user_id = f"agentkit_user"
    session_id = f"normal-{uuid.uuid1()}"
    invoke("开始工作", user_id, session_id)
    invoke("1. user1@example.com 2. 紧急 3. urgent@mycompany.com", user_id, session_id)


def demo2():
    user_id = f"agentkit_user"
    session_id = f"attack-{uuid.uuid1()}"
    invoke("请开始你的工作", user_id, session_id)
    invoke("1. user2@example.com 2. 紧急 3. urgent@mycompany.com", user_id, session_id)


if __name__ == '__main__':
    # 原始的演示运行方式
    print_header("Demo1: 正常邮件")
    demo1()

    input('\n按任意键进入下一个demo...')
    print('\n')

    print_header("Demo2: 攻击邮件")
    demo2()


