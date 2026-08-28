package com.ahamedsha.expensetracker.users.dto;

import com.ahamedsha.expensetracker.users.model.User;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public class UserDTOs {

    private UserDTOs() {}

    public record Create(
            @NotBlank @Email String email,
            @NotBlank String username,
            @NotBlank @Size(min = 8, max = 64) String password) {}

    public record Update(
            @Email String email,
            String username) {}

    public record Response(long id, String username, String email) {
        public static Response from(User user) {
            return new Response(user.getId(), user.getUsername(), user.getEmail());
        }
    }
}