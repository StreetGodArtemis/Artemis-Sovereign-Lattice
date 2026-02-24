import numpy as jnp
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ArtemisChronoEngine:
    in_dim: int
    out_dim: int
    hidden_dim: int = 128
    echo_decay: float = 0.95  # Increased from 0.7: Stronger internal memory
    rot_reg: float = 1e-2     # Increased from 1e-4: Heavier geometric constraint
    params: dict = field(default_factory=dict)
    opt_state: dict = field(default_factory=dict)

    def __post_init__(self):
        self.params['W1'] = jnp.random.randn(self.in_dim, self.hidden_dim) * jnp.sqrt(2.0 / self.in_dim)
        self.params['b1'] = jnp.zeros((self.hidden_dim,))
        self.params['W2'] = jnp.random.randn(self.hidden_dim, self.out_dim) * jnp.sqrt(2.0 / self.hidden_dim)
        self.params['b2'] = jnp.zeros((self.out_dim,))
        
        for k, v in self.params.items():
            self.opt_state['v'+k] = jnp.zeros_like(v)
            self.opt_state['g'+k+'_ema'] = jnp.zeros_like(v)

    def train_once(self, x, y, steps=1, lr=1e-3, momentum=0.9):
        mse_seq, rot_seq = [], []
        for _ in range(steps):
            # Forward
            h = jnp.tanh(x @ self.params['W1'] + self.params['b1'])
            y_pred = h @ self.params['W2'] + self.params['b2']
            
            # Loss
            error = y_pred - y
            mse = jnp.mean(error**2)
            
            W1 = self.params['W1']
            gram = W1.T @ W1
            rot_loss = jnp.sum((gram - jnp.eye(self.hidden_dim))**2)
            
            # Manual Backprop
            dy = 2.0 * error / x.shape[0]
            dW2 = h.T @ dy
            db2 = jnp.sum(dy, axis=0)
            
            dh = (dy @ self.params['W2'].T) * (1 - h**2)
            # Derivative of the rotational regularizer included here
            dW1 = x.T @ dh + self.rot_reg * (4.0 * W1 @ (gram - jnp.eye(self.hidden_dim)))
            db1 = jnp.sum(dh, axis=0)
            
            for k, grad in zip(['W1', 'b1', 'W2', 'b2'], [dW1, db1, dW2, db2]):
                ema = self.opt_state['g'+k+'_ema']
                v = self.opt_state['v'+k]
                
                g_mixed = 0.5 * grad + 0.5 * ema
                v_new = momentum * v - lr * g_mixed
                self.params[k] += v_new
                self.opt_state['v'+k] = v_new
                self.opt_state['g'+k+'_ema'] = self.echo_decay * ema + (1.0 - self.echo_decay) * grad
            
            mse_seq.append(mse)
            rot_seq.append(rot_loss)
            
        return {"mse_seq": mse_seq, "rot_seq": rot_seq, "final_loss": mse_seq[-1]}
