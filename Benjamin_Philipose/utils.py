import torch
import numpy as np


        
def save_checkpoint(model, optimizer, epoch, filename):
    checkpoint = {
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict()
    }
    torch.save(checkpoint, filename)

def load_checkpoint(filepath, model):
    checkpoint = torch.load(filepath)
    model.load_state_dict(checkpoint['model_state_dict'])
    epoch = checkpoint['epoch']
    return model, epoch

# Loss function
def mean_squared_error(x : np.ndarray, y : np.ndarray, theta : np.ndarray) -> np.ndarray:
    yhat = x @ theta 
    error = yhat - y 
    loss = (1 / len(y)) * np.sum(error ** 2) 
    return loss

# Gradient descent
def calculate_gradient_and_update(x: np.ndarray, y: np.ndarray, theta: np.ndarray, alpha: float) -> tuple([float, np.ndarray]):
    gradient = (1 / len(y)) * x.T @ ((x @ theta) - y) 
    theta_new = theta - (alpha * gradient) 
    loss = mean_squared_error(x, y, theta_new)
    return loss, theta_new

def cnn_train_step(model, dataloader, loss_fn, optimizer, device):
    model.train()
    losses_per_iteration = []
    for _ in range(dataloader.num_batches_per_epoch):
        optimizer.zero_grad()
        batch = dataloader.fetch_batch()       
        x_batch = batch['img_batch'].to(device)
        y_batch = batch['age_batch'].to(device)
        yhat = model(x_batch)
        yhat = torch.squeeze(yhat, 1)  # Ensure this matches your model output shape
        loss = loss_fn(yhat, y_batch)
        loss.backward()
        optimizer.step()
        losses_per_iteration.append(loss.item())
    return losses_per_iteration

def cnn_val_step(model, dataloader, loss_fn, device):
    model.eval()
    losses_per_iteration = []
    with torch.no_grad():
        for _ in range(dataloader.num_batches_per_epoch):
            batch = dataloader.fetch_batch()           
            x_batch = batch['img_batch'].to(device)
            y_batch = batch['age_batch'].to(device)
            yhat = model(x_batch)
            yhat = torch.squeeze(yhat, 1)  # Ensure this matches your model output shape
            loss = loss_fn(yhat, y_batch)
            losses_per_iteration.append(loss.item())
    return losses_per_iteration

def cnn_test_step(model, dataloader, device):
    model.eval()  # Set the model to evaluation mode

    predictions = []
    actuals = []

    with torch.no_grad():
        for _ in range(dataloader.num_batches_per_epoch):
            batch = dataloader.fetch_batch()
            x_batch = batch['img_batch'].to(device)
            y_batch = batch['age_batch'].to(device)
            yhat = model(x_batch)
            yhat = torch.squeeze(yhat, 1)  # Ensure this matches your model output shape
            predictions.extend(yhat.detach().cpu().numpy())
            actuals.extend(y_batch.detach().cpu().numpy())
    return predictions, actuals



def mmnn_train_step(model, dataloader, loss_fn, optimizer, device):
    model.train()
    losses_per_iteration = []
    for _ in range(dataloader.num_batches_per_epoch):
        optimizer.zero_grad()
        batch = dataloader.fetch_batch()
        x_batch = batch['img_batch'].to(device)
        num_features = batch['feat_batch'].to(device)
        y_batch = batch['age_batch'].to(device)
        yhat = model(x_batch, num_features)
        yhat = torch.squeeze(yhat, 1)  # Ensure this matches your model output shape
        loss = loss_fn(yhat, y_batch)
        loss.backward()
        optimizer.step()
        losses_per_iteration.append(loss.item())
    return losses_per_iteration

def mmnn_val_step(model, dataloader, loss_fn, device):
    model.eval()
    losses_per_iteration = []
    with torch.no_grad():
        for _ in range(dataloader.num_batches_per_epoch):
            batch = dataloader.fetch_batch()
            x_batch = batch['img_batch'].to(device)
            num_features = batch['feat_batch'].to(device)
            y_batch = batch['age_batch'].to(device)
            yhat = model(x_batch, num_features)
            yhat = torch.squeeze(yhat, 1)  # Ensure this matches your model output shape
            loss = loss_fn(yhat, y_batch)
            losses_per_iteration.append(loss.item())
    return losses_per_iteration

def mmnn_test_step(model, dataloader, device):
    model.eval()  # Set the model to evaluation mode

    predictions = []
    actuals = []

    with torch.no_grad():
        for _ in range(dataloader.num_batches_per_epoch):
            batch = dataloader.fetch_batch()
            x_batch = batch['img_batch'].to(device)
            num_features = batch['feat_batch'].to(device)
            y_batch = batch['age_batch'].to(device)

            yhat = model(x_batch, num_features)
            yhat = torch.squeeze(yhat, 1)  # Ensure this matches your model output shape

            predictions.extend(yhat.detach().cpu().numpy())
            actuals.extend(y_batch.detach().cpu().numpy())

    return predictions, actuals

