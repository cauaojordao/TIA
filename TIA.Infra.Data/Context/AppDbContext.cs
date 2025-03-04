using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using TIA.Domain.Entities;

namespace TIA.Persistence.Context
{
    public class AppDbContext : IdentityDbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        { }

        public DbSet<User> Users { get; set; }
        public DbSet<AppFile> AppFiles { get; set; }
        public DbSet<Question> Questions { get; set; }
        public DbSet<Answear> Answears { get; set; }

    }
}
