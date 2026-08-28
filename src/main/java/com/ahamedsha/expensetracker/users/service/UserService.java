package com.ahamedsha.expensetracker.users.service;

import com.ahamedsha.expensetracker.exception.ApiException;
import com.ahamedsha.expensetracker.users.dto.UserDTOs;
import com.ahamedsha.expensetracker.users.model.User;
import com.ahamedsha.expensetracker.users.repository.UserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public UserService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public User findById(long id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new ApiException.ResourceNotFoundException(id));
    }

    public User addUser(UserDTOs.Create request) {
        User user = User.builder()
                .username(request.username())
                .email(request.email())
                .password(passwordEncoder.encode(request.password()))
                .build();
        return userRepository.save(user);
    }

    public User updateUser(long id, UserDTOs.Update request) {
        User user = findById(id);
        Optional.ofNullable(request.username()).filter(s -> !s.isBlank()).ifPresent(user::setUsername);
        Optional.ofNullable(request.email()).filter(s -> !s.isBlank()).ifPresent(user::setEmail);
        return userRepository.save(user);
    }
}