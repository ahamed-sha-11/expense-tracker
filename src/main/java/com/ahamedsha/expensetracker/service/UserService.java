package com.ahamedsha.expensetracker.service;

import com.ahamedsha.expensetracker.dto.UserRequestDTO;
import com.ahamedsha.expensetracker.dto.UserResponseDTO;
import com.ahamedsha.expensetracker.exception.ApiException;
import com.ahamedsha.expensetracker.model.User;
import com.ahamedsha.expensetracker.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
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

    public User updateUser(UserRequestDTO userRequestDTO) {

        User user = findById(userRequestDTO.getId());
        Optional.ofNullable(userRequestDTO.getUsername()).ifPresent(user::setUsername);
        Optional.ofNullable(userRequestDTO.getEmail()).ifPresent(user::setEmail);

        return userRepository.save(user);
    }
}
