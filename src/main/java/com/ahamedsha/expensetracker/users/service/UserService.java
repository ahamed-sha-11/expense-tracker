package com.ahamedsha.expensetracker.users.service;

import com.ahamedsha.expensetracker.users.dto.UserRequestDTO;
import com.ahamedsha.expensetracker.exception.ApiException;
import com.ahamedsha.expensetracker.users.model.User;
import com.ahamedsha.expensetracker.users.repository.UserRepository;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import java.util.Optional;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder;

    public UserService(UserRepository userRepository, BCryptPasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public User findById(long id) {
        return userRepository.findById(id).orElseThrow(() -> new ApiException.ResourceNotFoundException(id));
    }

    public User addUser(UserRequestDTO userRequestDTO) {
        User user = User.builder()
                .username(userRequestDTO.getUsername())
                .email(userRequestDTO.getEmail())
                .password(passwordEncoder.encode(userRequestDTO.getPassword()))
                .build();

        return userRepository.save(user);
    }

    public User updateUser(long id, UserRequestDTO userRequestDTO) {

        User user = findById(id);
        Optional.ofNullable(userRequestDTO.getUsername()).ifPresent(user::setUsername);
        Optional.ofNullable(userRequestDTO.getEmail()).ifPresent(user::setEmail);

        return userRepository.save(user);
    }
}
