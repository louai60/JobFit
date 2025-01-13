import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
}

interface AuthState {
  isLoggedIn: boolean;
  user: User | null;
  error: string | null;
  isLoading: boolean;
}

const initialState: AuthState = {
  isLoggedIn: false,
  user: null,
  error: null,
  isLoading: false,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loginSuccess(state, action: PayloadAction<User>) {
      state.isLoggedIn = true;
      state.user = action.payload;
      state.error = null;
    },
    loginFailure(state, action: PayloadAction<string>) {
      state.isLoggedIn = false;
      state.user = null;
      state.error = action.payload;
    },
    registerSuccess(state, action: PayloadAction<User>) {
      state.isLoggedIn = true;
      state.user = action.payload;
      state.error = null;
    },
    registerFailure(state, action: PayloadAction<string>) {
      state.isLoggedIn = false;
      state.user = null;
      state.error = action.payload;
    },
    logout(state) {
      state.isLoggedIn = false;
      state.user = null;
      state.error = null;
    },
  },
});

export const { 
  loginSuccess, 
  loginFailure, 
  registerSuccess, 
  registerFailure, 
  logout 
} = authSlice.actions;

export default authSlice.reducer;