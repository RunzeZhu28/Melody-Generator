import torch
import torch.nn as nn

class LSTMModule(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, dropout_prob):
        super(LSTMModule, self).__init__()
        self.ident = torch.eye(input_size)
        self.hidden_size = hidden_size
        self.input_size = input_size
        # First LSTM Layer
        self.lstm1 = nn.LSTM(input_size, hidden_size, batch_first=True)
        # First Dropout Layer
        self.dropout1 = nn.Dropout(dropout_prob)
        # Second LSTM Layer
        self.lstm2 = nn.LSTM(hidden_size, hidden_size, batch_first=True)
        # Second Dropout Layer
        self.dropout2 = nn.Dropout(dropout_prob)
        # third LSTM Layer
        self.lstm3 = nn.LSTM(hidden_size, hidden_size, batch_first=True)

        # third Dropout Layer
        self.dropout3 = nn.Dropout(dropout_prob)
        self.fc = nn.Linear(hidden_size, output_size)
        #self.activation = nn.ReLU()  # Activation layer
        self.activation = nn.Softmax(dim=1)

    def forward(self, x):
        # Fix: You need put the self.ident on the cuda
        self.ident = self.ident.cuda()
        one_hot_list = [self.ident[t.long()] for t in x]
        one_hot = torch.stack(one_hot_list)
        one_hot = one_hot.view(x.shape[0], -1, self.input_size)

        # First LSTM Layer
        lstm1_output, (hidden1, _) = self.lstm1(one_hot)

        # First Dropout Layer
        lstm1_output = self.dropout1(lstm1_output)

        # Second LSTM Layer
        lstm2_output, (hidden2, _) = self.lstm2(lstm1_output)

        # Second Dropout Layer
        lstm2_output = self.dropout2(lstm2_output)

        hidden = lstm2_output[:, -1, :]  # Take the hidden state of the last time step
        output = self.activation(output)  # Apply activation function
        output = self.fc(hidden)
        return output
