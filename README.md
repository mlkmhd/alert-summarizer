# Summarization of Email Alerts Using LLM

Background: As we receive numerous email notifications daily, reading each one individually is time-consuming and may lead to missing important details. There is a need for a tool that can summarize alerts layer by layer, enhancing decision-making regarding whether to act on a specific alert.

Here are the different levels of summarization:

<p align="center">
  <img src="overview.png?raw=true" />
</p>

Algorithm Description:

In each level of summarization, the algorithm reduces the previous layer by half. For example, in the image above, at Level 1, there are 10 files, each containing an alert. The algorithm merges every two alerts into one summarized alert that encapsulates both. Therefore, after the first level of summarization, the algorithm converts 10 files into 5 files. This algorithm is recursive and continues until only one summarized file remains. I've utilized Ollama, a popular LLM tool, for summarizing email content.