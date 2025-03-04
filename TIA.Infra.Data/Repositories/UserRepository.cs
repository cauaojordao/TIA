using Microsoft.EntityFrameworkCore;
using TIA.Domain.Entities;
using TIA.Domain.Interfaces;
using TIA.Persistence.Context;

namespace TIA.Persistence.Repositories
{
    public class UserRepository : BaseRepository<User>, IUserRepository
    {
        public UserRepository(AppDbContext context) : base(context)
        { }

        public async Task<User> GetByEmail(string email, CancellationToken cancellationToken)
        {
            return await Context.Users.FirstOrDefaultAsync(x => x.Email == email, cancellationToken);
        }
    }
}
