
using Microsoft.AspNetCore.Identity;
using TIA.Application.Interfaces;
using TIA.Application.Services.Identity;
using TIA.Domain.Entities;

namespace TIA.Application.Identity
{
    public class IdentityService : IIdentityService
    {
        private readonly UserManager<IdentityUser> _userManager;
        private readonly RoleManager<IdentityRole> _roleManager;

        public IdentityService(UserManager<IdentityUser> userManager, RoleManager<IdentityRole> roleManager)
        {
            _userManager = userManager;
            _roleManager = roleManager;
        }

        public async Task<IdentityResult> RegisterUser(RegisterUserDto dto)
        {
            var identityUser = new IdentityUser
            {
                UserName = dto.Username,
                Email = dto.Email
            };

            var user = new User
            {
                Username = dto.Username,
                Email = dto.Email,
            };

            var result = await _userManager.CreateAsync(identityUser, dto.Password);

            if (result.Succeeded)
            {
                await _userManager.AddToRoleAsync(identityUser, "User");

            }

            return result;
        }

        public async Task<User?> GetUserByEmailAsync(RegisterUserDto dto)
        {
            var identityUser = await _userManager.FindByEmailAsync(dto.Email);

            if (identityUser == null) return null;

            return new User
            {
                Username = identityUser.UserName!,
                Email = identityUser.Email!,
            };
        }

    }

}
