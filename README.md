## "Streaming with SSE Events using Zypher"

Server-Sent Events (SSE) is a standard that describes how servers can initiate data transmission towards browser clients once an initial client connection has been established. It’s particularly useful for creating a one-way communication channel from the server to the client, such as for real-time notifications, live updates, and streaming data.


Server-Sent Events (SSE) can be enabled and configured independently for each model using the IS_STREAMING_OUTPUT property in the model configuration. You can use the 'stream_output_handler' to send each event and close the event stream. There are some limitations in streaming the type of input

- Only INT, STRING, BOOLEAN are supported as the datatypes in the INPUT 
- The shape of the parameter should be [1], multiple inputs or objects are by using "json.dumps(object)" and then passed as string 
- Output should have the same schema in all the iterative responses 

#### Create a custom runtime

To get started with importing the template for the streaming create a Custom runtime with the 'inferless-runtime-config.yaml' also use cuda_version as **12.4.1**
Define  IS_STREAMING_OUTPUT in the **input\_schema.py**

```python
/
├── app.py
├── input_schema.py 
```

input\_schema.py 

```input_schema
IS_STREAMING_OUTPUT = True
```

```
in app.py 

# Sent the partial response as an event 
stream_output_handler.send_streamed_output(output_dict)

# Call this to close the stream, If not called can lead to the issue of request not being released
stream_output_handler.finalise_streamed_output()

```


### Key Advantages of Using SSE

1. Simplicity: SSE is straightforward to implement both on the server and the client side. Unlike WebSockets, which require a special protocol and server setup, SSE works over standard HTTP and can be handled by traditional web servers without any special configuration.

2. Efficient Real-time Communication: SSE is designed for scenarios where the server needs to push data to the client. It’s very efficient for use cases like live notifications, feeds, and real-time analytics dashboards where updates are frequent and originate from the server.

3. Built-in Reconnection: SSE has automatic reconnection support. If the connection between the client and server is lost, the client will automatically attempt to reestablish the connection after a timeout. This makes it resilient and ensures continuous data flow without manual intervention.
