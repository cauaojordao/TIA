using Microsoft.AspNetCore.Identity;
using TIA.Application.Services.Identity;
using TIA.Domain.Entities;

namespace TIA.Application.Interfaces
{
    public interface IIdentityService
    {
        Task<IdentityResult> RegisterUser(RegisterUserDto dto);
        Task<User?> GetUserByEmailAsync(RegisterUserDto dto);
    }
}
