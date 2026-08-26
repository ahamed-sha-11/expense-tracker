package com.ahamedsha.expensetracker.dto;

import lombok.Data;

@Data
public class UserRequestDTO {
    private String email;
    private String username;
    private String password;
}
