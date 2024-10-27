import json
import ollama
import html2text
import os
from pathlib import Path


def summarize(result_dir, summarize_len):

    files = os.listdir(f'results/{result_dir}')
    files.sort()
    if len(files) == 1:
        return

    combined_files = []
    for i in range(0, len(files), 2):
        if i + 1 < len(files):
            with open(os.path.join(f'results/{result_dir}', files[i]), 'r') as file1:
                content1 = file1.read()
            with open(os.path.join(f'results/{result_dir}', files[i + 1]), 'r') as file2:
                content2 = file2.read()

            # Combine the content
            combined_content = 'first alert:\n' + content1 + '\nsecond alert:\n' + content2
            summarized_combined_content = summarize_using_ollama(combined_content, round(summarize_len))

            # Create a new combined file name
            combined_file_name = f'{i//2 + 1}.txt'
            combined_output_dir = f'results/{result_dir+1}'
            Path(combined_output_dir).mkdir(parents=True, exist_ok=True)
            with open(os.path.join(combined_output_dir, combined_file_name), 'w') as combined_file:
                combined_file.write(summarized_combined_content)

            combined_files.append(combined_file_name)

        else:
            combined_output_dir = f'results/{result_dir+1}'
            Path(combined_output_dir).mkdir(parents=True, exist_ok=True)
            with open(os.path.join(f'results/{result_dir}', files[i]), 'r') as file:
                content = file.read()
            combined_file_name = f'{i//2 + 1}.txt'
            with open(os.path.join(combined_output_dir, combined_file_name), 'w') as combined_file:
                combined_file.write(content)

            combined_files.append(combined_file_name)
    summarize(result_dir+1, round(summarize_len*1.5))


def summarize_using_ollama(content, summarization_size):
    response = ollama.chat(
        model='llama3.1:8b',
        messages=[
            {
                'role': "system",
                'content': f"You have to provide a summarize (without any preface) of provided text by the user up to {summarization_size} words"
            },
            {
                'role': 'user',
                'content': content
            }
        ],
        stream=False,
    )

    return response['message']['content']


if __name__ == '__main__':
    with open('emails.json', 'r') as file:
        data = json.load(file)

    emails = data['value']
    counter = 1
    Path('results/1').mkdir(parents=True, exist_ok=True)
    for email in emails:
        body = html2text.html2text(email["body"]['content'])
        summarized_content = summarize_using_ollama(body, 100)
        email_file_name = f'results/1/{counter}.txt'
        with open(email_file_name, 'w') as file:
            file.write(summarized_content)
        counter += 1
    summarize(1, round(100 * 1.5))
